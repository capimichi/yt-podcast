"""Module for ytpodcast.client.yt_api_client."""

from datetime import timedelta
from typing import Any

from isodate import parse_duration
from isodate.duration import Duration
from pyyoutube import Client
from pyyoutube.models.channel import ChannelListResponse
from pyyoutube.models.video import VideoListResponse

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.client.ytapi.video_response import VideoResponse


class YtApiClient:
    """Client wrapper for the YouTube Data API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Store API configuration."""
        self.base_url: str = base_url.rstrip("/")
        self.api_key: str
        self.client: Client = Client(api_key=api_key)

    def fetch_channel(self, identifier: str) -> ChannelResponse:
        """Fetch a channel payload from the YouTube API."""
        channel_params: dict[str, str] = {}
        if identifier.startswith("@"):
            channel_params["for_handle"] = identifier
        elif identifier.startswith("UC") and len(identifier) == 24:
            channel_params["channel_id"] = identifier
        else:
            channel_params["for_username"] = identifier

        response: ChannelListResponse = self.client.channels.list(
            parts="snippet",
            return_json=False,
            **channel_params,
        )

        items: list[Any] = response.items
        if not items:
            raise ValueError(f"Channel not found for identifier '{identifier}'.")

        item = items[0]
        snippet = item.snippet
        channel_id: str = item.id or identifier
        return ChannelResponse(
            channel_id=channel_id,
            title=snippet.title or "",
            description=snippet.description or "",
            url=f"https://www.youtube.com/channel/{channel_id}",
        )

    def fetch_video(self, video_id: str) -> VideoResponse:
        """Fetch a video payload from the YouTube API."""

        response: VideoListResponse = self.client.videos.list(
            parts="snippet,contentDetails",
            video_id=video_id,
            return_json=False,
        )
        items: list[Any] = response.items
        if not items:
            raise ValueError(f"Video not found for id '{video_id}'.")

        item = items[0]
        snippet = item.snippet
        content_details = item.contentDetails
        duration_iso: str = content_details.duration or "PT0S"
        duration: timedelta | Duration = parse_duration(duration_iso)
        duration_seconds: int = (
            int(duration.total_seconds()) if isinstance(duration, timedelta) else 0
        )

        channel_id: str = snippet.channelId or ""
        return VideoResponse(
            video_id=item.id or video_id,
            title=snippet.title or "",
            description=snippet.description or "",
            duration_seconds=duration_seconds,
            url=f"https://www.youtube.com/watch?v={video_id}",
            channel_id=channel_id,
        )
