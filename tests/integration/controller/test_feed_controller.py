"""Integration tests for ytpodcast.controller.feed_controller."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from ytpodcast.api import app
from ytpodcast.container.default_container import DefaultContainer


class TestFeedController(unittest.TestCase):
    """Integration tests for the feed controller."""

    client: TestClient
    channel_handle = "@francescocosta21"

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the client for integration calls."""
        container = DefaultContainer.get_instance()
        api_key = container.get_var("yt_api_key")
        if not api_key:
            raise unittest.SkipTest("YT_API_KEY is not set.")

        cls.client = TestClient(app)

    def test_get_channel_feed_xml(self) -> None:
        """Fetch a channel feed in RSS XML format."""
        response = self.client.get(f"/feeds/{self.channel_handle}/xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/rss+xml", response.headers.get("content-type", ""))
        self.assertIn("<rss", response.text)
        self.assertIn("<channel>", response.text)
