"""Module for ytpodcast.helper.file_helper."""

import mimetypes
import os
from pathlib import Path


# pylint: disable=too-few-public-methods
class FileHelper:
    """Helper for file-related operations."""

    def resolve_media_type(self, file_path: Path) -> str:
        """Resolve a media type from a file path."""
        media_type, _ = mimetypes.guess_type(str(file_path))
        return media_type or "application/octet-stream"

    def ensure_directory(self, directory_path: Path) -> Path:
        """Ensure that a directory exists."""
        directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path

    def resolve_download_path(self, download_dir: str, video_id: str) -> Path:
        """Resolve the output path for a downloaded audio file."""
        return Path(download_dir) / f"{video_id}.mp3"

    def create_placeholder_file(self, file_path: Path) -> Path:
        """Create an empty placeholder file when missing."""
        self.ensure_directory(file_path.parent)
        if not file_path.exists():
            file_path.touch()
        return file_path

    def get_file_size(self, file_path: Path) -> int:
        """Return the file size, or zero when it is missing."""
        if not file_path.exists():
            return 0
        return file_path.stat().st_size

    def is_non_empty_file(self, file_path: Path) -> bool:
        """Return True when a file exists and is not empty."""
        return file_path.exists() and self.get_file_size(file_path) > 0

    def list_zero_byte_files(self, directory_path: Path, pattern: str = "*.mp3") -> list[Path]:
        """Return zero-byte files matching the provided pattern."""
        if not directory_path.exists():
            return []
        return [
            path
            for path in sorted(directory_path.glob(pattern))
            if path.is_file() and self.get_file_size(path) == 0
        ]

    def replace_file_atomically(self, source_path: Path, destination_path: Path) -> None:
        """Atomically replace a destination file with a source file."""
        self.ensure_directory(destination_path.parent)
        os.replace(source_path, destination_path)
