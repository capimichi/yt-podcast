"""Integration tests for ytpodcast.client.yt_dl_client."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ytpodcast.client.yt_dl_client import YtDlClient


class TestYtDlClient(unittest.TestCase):
    """Integration tests for the yt-dlp client."""

    video_id = "TpeQKp0WcfQ"

    def test_download_audio(self) -> None:
        """Download an audio file for a sample video."""
        try:
            import yt_dlp  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("yt-dlp is not installed.") from exc

        with tempfile.TemporaryDirectory() as temp_dir:
            client = YtDlClient(default_format="bestaudio", download_dir=temp_dir)
            formats = client.fetch_audio_formats(self.video_id)
            self.assertTrue(formats)
            result_path = client.download_audio(self.video_id)
            expected_path = Path(temp_dir) / f"{self.video_id}{result_path.suffix}"
            self.assertTrue(result_path.exists())
            self.assertEqual(result_path, expected_path)
