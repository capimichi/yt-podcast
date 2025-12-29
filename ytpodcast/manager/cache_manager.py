"""Module for ytpodcast.manager.cache_manager."""

import json
from datetime import datetime
from datetime import timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ytpodcast.model.service.cache_entry import CacheEntry


# pylint: disable=too-few-public-methods
class CacheManager:
    """Filesystem-backed cache storage."""

    def __init__(self, cache_dir: str) -> None:
        """Store the cache directory."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def create_cache_key(self, *args: Any, **kwargs: Any) -> str:
        """Return a deterministic cache key from inputs."""
        payload: dict[str, Any] = {
            "args": self._normalize_payload(args),
            "kwargs": self._normalize_payload(kwargs),
        }
        serialized: str = json.dumps(payload, sort_keys=True, default=str)
        return sha256(serialized.encode("utf-8")).hexdigest()

    def cretate_cache_key(self, *args: Any, **kwargs: Any) -> str:
        """Backwards-compatible typo alias for create_cache_key."""
        return self.create_cache_key(*args, **kwargs)

    def get(self, key: str) -> str | None:
        """Return cached content if it is still valid."""
        cache_path: Path = self._build_cache_path(key)
        if not cache_path.exists():
            return None
        try:
            data: dict[str, Any] = json.loads(cache_path.read_text(encoding="utf-8"))
            entry: CacheEntry = CacheEntry.model_validate(data)
        except (json.JSONDecodeError, OSError, ValidationError):
            return None
        expires_at: datetime = entry.get_expires_at()
        if expires_at <= self._now_utc():
            return None
        return entry.get_value()

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        """Store content with a TTL in seconds."""
        expires_at: float = self._now_utc().timestamp() + ttl_seconds
        expires_at_value: datetime = datetime.fromtimestamp(expires_at, tz=timezone.utc)
        entry: CacheEntry = CacheEntry(expires_at=expires_at_value, value=value)
        cache_path: Path = self._build_cache_path(key)
        cache_path.write_text(
            json.dumps(entry.model_dump(mode="json"), ensure_ascii=True),
            encoding="utf-8",
        )

    def _build_cache_path(self, key: str) -> Path:
        """Return the filesystem path for the cache key."""
        return self.cache_dir / f"{key}.json"

    def _now_utc(self) -> datetime:
        """Return the current UTC timestamp."""
        return datetime.now(timezone.utc)

    def _normalize_payload(self, value: Any) -> Any:
        """Normalize values for stable serialization."""
        if isinstance(value, dict):
            return {key: self._normalize_payload(val) for key, val in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._normalize_payload(item) for item in value]
        if isinstance(value, datetime):
            normalized: datetime = value
            if normalized.tzinfo is None:
                normalized = normalized.replace(tzinfo=timezone.utc)
            return normalized.astimezone(timezone.utc).isoformat()
        return value
