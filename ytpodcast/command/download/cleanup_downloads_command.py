"""CLI command for removing expired downloaded audio files."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone

import click
from injector import inject

from ytpodcast.command.abstract_command import AbstractCommand
from ytpodcast.service.download_cleanup_service import DownloadCleanupService


class CleanupDownloadsCommand(AbstractCommand):
    """Command that removes old downloaded audio files."""

    command_name = "download:cleanup"

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        download_cleanup_service: DownloadCleanupService,
    ) -> None:
        """Store dependencies for download cleanup processing."""
        self.download_cleanup_service = download_cleanup_service

    def run(self) -> None:
        """Delete downloaded audio files older than the configured retention."""
        started_at: str = datetime.now(timezone.utc).isoformat()
        retention_days: int = self.download_cleanup_service.get_retention_days()
        click.echo(
            f"[{started_at}] Starting download cleanup with retention {retention_days} days."
        )
        deleted_count: int = self.download_cleanup_service.cleanup_downloads()
        completed_at: str = datetime.now(timezone.utc).isoformat()
        click.echo(f"[{completed_at}] Deleted {deleted_count} expired downloads.")
