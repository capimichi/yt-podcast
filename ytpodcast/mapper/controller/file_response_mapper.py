"""Module for ytpodcast.mapper.controller.file_response_mapper."""

from pathlib import Path

from fastapi.responses import FileResponse

from ytpodcast.helper.file_helper import FileHelper


# pylint: disable=too-few-public-methods
class FileResponseMapper:
    """Build file responses from domain models."""

    def __init__(self, file_helper: FileHelper) -> None:
        """Store helper dependencies."""
        self.file_helper = file_helper

    def create_from_path(self, download_path: Path) -> FileResponse:
        """Convert a downloaded audio path into a file response."""
        media_type: str = self.file_helper.resolve_media_type(download_path)
        return FileResponse(
            path=str(download_path),
            media_type=media_type,
            filename=download_path.name,
        )
