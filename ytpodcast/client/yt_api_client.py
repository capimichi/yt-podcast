"""Module for ytpodcast.client.yt_api_client."""

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.client.ytapi.video_response import VideoResponse


class YtApiClient:
    """Client wrapper for the YouTube Data API (stubbed)."""

    def __init__(self, base_url: str, api_key: str | None) -> None:
        """Store API configuration."""
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def fetch_channel(self, identifier: str) -> ChannelResponse:
        """Return a stubbed channel payload."""
        return ChannelResponse(
            channel_id=identifier,
            title=f"Channel {identifier}",
            description="Sample channel description",
            url=f"{self.base_url}/channels/{identifier}",
        )

    def fetch_video(self, video_id: str) -> VideoResponse:
        """Return a stubbed video payload."""
        return VideoResponse(
            video_id=video_id,
            title=f"Video {video_id}",
            description="Sample video description",
            duration_seconds=0,
            url=f"{self.base_url}/videos/{video_id}",
            channel_id="sample-channel",
        )
