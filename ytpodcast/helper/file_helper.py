"""Module for ytpodcast.helper.file_helper."""

import mimetypes
from pathlib import Path


# pylint: disable=too-few-public-methods
class FileHelper:
    """Helper for file-related operations."""

    def resolve_media_type(self, file_path: Path) -> str:
        """Resolve a media type from a file path."""
        media_type, _ = mimetypes.guess_type(str(file_path))
        return media_type or "application/octet-stream"
