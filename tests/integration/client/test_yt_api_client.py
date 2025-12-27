"""Integration tests for ytpodcast.client.yt_api_client."""

from __future__ import annotations

import unittest

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.client.ytapi.video_response import VideoResponse
from ytpodcast.container.default_container import DefaultContainer


class TestYtApiClient(unittest.TestCase):
    """Integration tests for the YouTube API client."""

    api_key: str
    client: YtApiClient
    channel_handle = "@francescocosta21"
    video_id = "FEtPLvsBS2M"

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize the client for integration calls."""
        container = DefaultContainer.get_instance()
        api_key = container.get_var("yt_api_key")
        if not api_key:
            raise unittest.SkipTest("YT_API_KEY is not set.")

        cls.api_key = api_key
        cls.client = container.get(YtApiClient)

    def test_fetch_channel_by_handle(self) -> None:
        """Fetch a channel by handle."""
        response: ChannelResponse = self.client.fetch_channel(self.channel_handle)
        self.assertTrue(response.channel_id)
        self.assertTrue(response.title)
        self.assertIn(response.channel_id, response.url)

    def test_fetch_video_by_id(self) -> None:
        """Fetch a video by id."""
        response: VideoResponse = self.client.fetch_video(self.video_id)
        self.assertEqual(response.video_id, self.video_id)
        self.assertTrue(response.title)
        self.assertTrue(response.channel_id)
        self.assertIn(self.video_id, response.url)
