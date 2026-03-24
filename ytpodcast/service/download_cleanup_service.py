"""Module for ytpodcast.service.download_cleanup_service."""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path

from ytpodcast.helper.file_helper import FileHelper


# pylint: disable=too-few-public-methods
class DownloadCleanupService:
    """Service layer for removing expired downloaded audio files."""

    def __init__(
        self,
        file_helper: FileHelper,
        download_dir: str,
        retention_days: int,
    ) -> None:
        """Store dependencies for download cleanup processing."""
        self.file_helper = file_helper
        self.download_dir_path = Path(download_dir)
        self.retention_days = retention_days

    def cleanup_downloads(self) -> int:
        """Delete downloaded audio files older than the configured retention."""
        self.file_helper.ensure_directory(self.download_dir_path)
        cutoff_at: datetime = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        deleted_count: int = 0
        for download_path in self.file_helper.list_non_empty_files(self.download_dir_path):
            if self.file_helper.get_last_modified_at(download_path) >= cutoff_at:
                continue
            self._log(f"Deleting expired download '{download_path.name}'.")
            self.file_helper.delete_file(download_path)
            deleted_count += 1
        return deleted_count

    def get_retention_days(self) -> int:
        """Return the configured retention period in days."""
        return self.retention_days

    def _log(self, message: str) -> None:
        """Write a timestamped log message for the cleanup worker."""
        timestamp: str = datetime.now(timezone.utc).isoformat()
        print(f"[{timestamp}] {message}")
