"""Module for ytpodcast.service.pending_download_service."""

import fcntl
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from ytpodcast.helper.file_helper import FileHelper
from ytpodcast.service.video_service import VideoService


# pylint: disable=too-few-public-methods
class PendingDownloadService:
    """Service layer for processing queued zero-byte downloads."""

    def __init__(
        self,
        video_service: VideoService,
        file_helper: FileHelper,
        download_dir: str,
    ) -> None:
        """Store dependencies for pending download processing."""
        self.video_service = video_service
        self.file_helper = file_helper
        self.download_dir_path = Path(download_dir)
        self.locks_dir_path = self.download_dir_path / ".locks"

    def process_pending_downloads(self) -> int:
        """Download and replace every pending zero-byte placeholder."""
        self.file_helper.ensure_directory(self.download_dir_path)
        self.file_helper.ensure_directory(self.locks_dir_path)
        processed_count: int = 0
        pending_paths: list[Path] = self.file_helper.list_zero_byte_files(
            self.download_dir_path
        )
        for pending_path in pending_paths:
            video_id: str = pending_path.stem
            with self._acquire_lock(video_id) as is_locked:
                if not is_locked:
                    continue
                if self.file_helper.get_file_size(pending_path) != 0:
                    continue
                processed_path: Path = self._process_pending_path(video_id, pending_path)
                if self.file_helper.is_non_empty_file(processed_path):
                    processed_count += 1
        return processed_count

    def _process_pending_path(self, video_id: str, pending_path: Path) -> Path:
        """Materialize a single pending placeholder and replace it atomically."""
        with TemporaryDirectory() as temp_dir:
            temp_dir_path: Path = Path(temp_dir)
            temp_output_path: Path = temp_dir_path / pending_path.name
            downloaded_path: Path = self.video_service.materialize_audio_download(
                video_id,
                temp_output_path,
            )
            if not self.file_helper.is_non_empty_file(downloaded_path):
                raise ValueError(
                    f"Downloaded file for '{video_id}' is missing or still empty."
                )
            self.file_helper.replace_file_atomically(downloaded_path, pending_path)
        return pending_path

    @contextmanager
    def _acquire_lock(self, video_id: str) -> Iterator[bool]:
        """Acquire an exclusive non-blocking filesystem lock for one video."""
        lock_path: Path = self.locks_dir_path / f"{video_id}.lock"
        self.file_helper.ensure_directory(lock_path.parent)
        with lock_path.open("a+", encoding="utf-8") as lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                yield False
                return
            try:
                yield True
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
