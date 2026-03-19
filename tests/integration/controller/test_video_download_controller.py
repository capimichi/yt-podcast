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
    video_id = "FEtPLvsBS2M"

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the client for integration calls."""
        cls.client = TestClient(app)

    def setUp(self) -> None:
        """Remove any leftover test download files."""
        container = DefaultContainer.get_instance()
        download_dir = Path(container.get_var("download_dir"))
        self.download_path = download_dir / f"{self.video_id}.mp3"
        if self.download_path.exists():
            self.download_path.unlink()

    def tearDown(self) -> None:
        """Remove test download files after each assertion."""
        if self.download_path.exists():
            self.download_path.unlink()

    def test_download_video_audio_returns_ready_file(self) -> None:
        """Return the existing audio file when it is ready."""
        self.download_path.parent.mkdir(parents=True, exist_ok=True)
        self.download_path.write_bytes(b"ready")
        response = self.client.get(f"/videos/{self.video_id}/download")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_download_video_audio_returns_conflict_for_pending_file(self) -> None:
        """Return a conflict while the audio file is still pending."""
        response = self.client.get(f"/videos/{self.video_id}/download")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"]["code"], "download_not_ready")
        self.assertEqual(response.headers.get("retry-after"), "60")
        self.assertTrue(self.download_path.exists())
        self.assertEqual(self.download_path.stat().st_size, 0)
