"""Integration tests for ytpodcast.controller.video_controller download routes."""

from __future__ import annotations

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from ytpodcast.api import app
from ytpodcast.container.default_container import DefaultContainer


class TestVideoDownloadController(unittest.TestCase):
    """Integration tests for video download routes."""

    client: TestClient
    video_id = "TpeQKp0WcfQ"

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the client for integration calls."""
        try:
            import yt_dlp  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("yt-dlp is not installed.") from exc

        cls.client = TestClient(app)

    def test_download_video_audio(self) -> None:
        """Download an audio file via the API."""
        response = self.client.get(f"/videos/{self.video_id}/download")
        self.assertEqual(response.status_code, 200)
        container = DefaultContainer.get_instance()
        download_dir = container.get_var("download_dir")
        downloaded_files = list(Path(download_dir).glob(f"{self.video_id}.*"))
        self.assertTrue(downloaded_files)
