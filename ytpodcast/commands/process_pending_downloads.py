"""CLI command for ytpodcast pending download processing."""

from ytpodcast.container.default_container import DefaultContainer
from ytpodcast.service.pending_download_service import PendingDownloadService


def main() -> None:
    """Process every queued download placeholder."""
    container: DefaultContainer = DefaultContainer.get_instance()
    pending_download_service: PendingDownloadService = container.get(
        PendingDownloadService
    )
    processed_count: int = pending_download_service.process_pending_downloads()
    print(f"Processed {processed_count} pending downloads.")


if __name__ == "__main__":
    main()
