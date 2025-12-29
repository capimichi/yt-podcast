"""Module for ytpodcast.model.service.cache_entry."""

from datetime import datetime

from pydantic import BaseModel


class CacheEntry(BaseModel):
    """Domain model for cache entries."""

    expires_at: datetime
    value: str

    def get_expires_at(self) -> datetime:
        """Return the expiration timestamp."""
        return self.expires_at

    def get_value(self) -> str:
        """Return the cached value."""
        return self.value
