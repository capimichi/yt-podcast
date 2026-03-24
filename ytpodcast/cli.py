"""Command line entrypoint for ytpodcast."""

from __future__ import annotations

import click

from ytpodcast.command.download.cleanup_downloads_command import CleanupDownloadsCommand
from ytpodcast.command.download.process_pending_downloads_command import ProcessPendingDownloadsCommand
from ytpodcast.container.default_container import DefaultContainer


@click.group()
def cli() -> None:
    """Command line entrypoint for ytpodcast."""


default_container: DefaultContainer = DefaultContainer.get_instance()

cli.add_command(default_container.get(CleanupDownloadsCommand).to_click_command())
cli.add_command(default_container.get(ProcessPendingDownloadsCommand).to_click_command())


if __name__ == "__main__":
    cli()
