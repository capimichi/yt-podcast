"""Integration tests for ytpodcast.client.yt_dl_client."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from ytpodcast.client.yt_dl_client import YtDlClient


class TestYtDlClient(unittest.TestCase):
    """Integration tests for the yt-dlp client."""

    video_id = "FEtPLvsBS2M"

    def test_fetch_audio_format(self) -> None:
        """Fetch the default audio format payload."""
        if shutil.which("yt-dlp") is None:
            raise unittest.SkipTest("yt-dlp is not installed.")

        with tempfile.TemporaryDirectory() as temp_dir:
            client = YtDlClient(
                default_format="bestaudio",
                download_dir=temp_dir,
                ytdl_executable_path="yt-dlp",
                ffmpeg_executable_path="ffmpeg",
            )
            default_format = client.fetch_audio_format(self.video_id)
            self.assertTrue(default_format.get_format_id())
            self.assertTrue(default_format.get_extension())
            self.assertTrue(default_format.get_is_audio_only())

    def test_fetch_audio_formats(self) -> None:
        """Fetch available audio formats for a video."""
        if shutil.which("yt-dlp") is None:
            raise unittest.SkipTest("yt-dlp is not installed.")

        with tempfile.TemporaryDirectory() as temp_dir:
            client = YtDlClient(
                default_format="bestaudio",
                download_dir=temp_dir,
                ytdl_executable_path="yt-dlp",
                ffmpeg_executable_path="ffmpeg",
            )
            formats = client.fetch_audio_formats(self.video_id)
            self.assertTrue(formats)

    def test_download_audio(self) -> None:
        """Download an audio file for a sample video."""
        if shutil.which("yt-dlp") is None:
            raise unittest.SkipTest("yt-dlp is not installed.")
        if shutil.which("ffmpeg") is None:
            raise unittest.SkipTest("ffmpeg is not installed.")

        with tempfile.TemporaryDirectory() as temp_dir:
            client = YtDlClient(
                default_format="bestaudio",
                download_dir=temp_dir,
                ytdl_executable_path="yt-dlp",
                ffmpeg_executable_path="ffmpeg",
            )
            formats = client.fetch_audio_formats(self.video_id)
            audio_only = [
                format_item for format_item in formats if format_item.get_is_audio_only()
            ]
            candidates = audio_only or formats
            selected_format = candidates[0]
            result_path = client.download_audio(
                self.video_id,
                selected_format.get_format_id(),
            )
            expected_path = Path(temp_dir) / f"{self.video_id}{result_path.suffix}"
            self.assertTrue(result_path.exists())
            self.assertEqual(result_path, expected_path)
