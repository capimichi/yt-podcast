"""CLI command for processing pending audio downloads."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone

import click
from injector import inject

from ytpodcast.command.abstract_command import AbstractCommand
from ytpodcast.service.pending_download_service import PendingDownloadService


class ProcessPendingDownloadsCommand(AbstractCommand):
    """Command that materializes queued audio downloads."""

    command_name = "download:process-pending"

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        pending_download_service: PendingDownloadService,
    ) -> None:
        """Store dependencies for pending download processing."""
        self.pending_download_service = pending_download_service

    def run(self) -> None:
        """Process every queued download placeholder."""
        started_at: str = datetime.now(timezone.utc).isoformat()
        click.echo(f"[{started_at}] Starting pending download processing.")
        processed_count: int = self.pending_download_service.process_pending_downloads()
        completed_at: str = datetime.now(timezone.utc).isoformat()
        click.echo(f"[{completed_at}] Processed {processed_count} pending downloads.")
