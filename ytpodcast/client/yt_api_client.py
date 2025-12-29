"""Module for ytpodcast.client.yt_api_client."""

from datetime import datetime
from datetime import timezone
from typing import Any

from pyyoutube import Client
from pyyoutube.models.channel import ChannelListResponse
from pyyoutube.models.video import VideoListResponse

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.client.ytapi.channel_video_response import ChannelVideoResponse
from ytpodcast.model.client.ytapi.channel_videos_page_response import ChannelVideosPageResponse
from ytpodcast.model.client.ytapi.video_response import VideoResponse
from ytpodcast.mapper.client.ytapi.channel_response_mapper import ChannelResponseMapper
from ytpodcast.mapper.client.ytapi.video_response_mapper import VideoResponseMapper


class YtApiClient:
    """Client wrapper for the YouTube Data API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        channel_response_mapper: ChannelResponseMapper,
        video_response_mapper: VideoResponseMapper,
    ) -> None:
        """Store API configuration."""
        self.base_url: str = base_url.rstrip("/")
        self.api_key: str
        self.client: Client = Client(api_key=api_key)
        self.channel_response_mapper = channel_response_mapper
        self.video_response_mapper = video_response_mapper

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

        return self.channel_response_mapper.create_from_channel_list_response(
            response,
            identifier,
        )

    def fetch_video(self, video_id: str) -> VideoResponse:
        """Fetch a video payload from the YouTube API."""

        response: VideoListResponse = self.client.videos.list(
            parts="snippet,contentDetails",
            video_id=video_id,
            return_json=False,
        )
        return self.video_response_mapper.create_from_video_list_response(
            response,
            video_id,
        )

    def fetch_channel_videos_page(
        self,
        channel_id: str,
        max_results: int = 20,
        page_token: str | None = None,
    ) -> ChannelVideosPageResponse:
        """Fetch a page of channel videos for feed generation."""
        response: Any = self.client.search.list(
            part="snippet",
            channel_id=channel_id,
            order="date",
            type="video",
            max_results=max_results,
            page_token=page_token,
            return_json=False,
        )
        items: list[Any] = response.items
        videos: list[ChannelVideoResponse] = []
        for item in items:
            snippet = item.snippet
            video_id_value: str = item.id.videoId or ""
            if not video_id_value:
                continue
            published_at_value: datetime = self._normalize_published_at(
                snippet.publishedAt
            )
            videos.append(
                ChannelVideoResponse(
                    video_id=video_id_value,
                    title=snippet.title or "",
                    description=snippet.description or "",
                    url=f"https://www.youtube.com/watch?v={video_id_value}",
                    published_at=published_at_value,
                )
            )
        next_page_token: str | None = getattr(response, "nextPageToken", None)
        return ChannelVideosPageResponse(items=videos, next_page_token=next_page_token)

    def _normalize_published_at(self, published_at: Any) -> datetime:
        """Normalize published timestamps into timezone-aware datetimes."""
        if isinstance(published_at, datetime):
            if published_at.tzinfo is None:
                return published_at.replace(tzinfo=timezone.utc)
            return published_at
        if isinstance(published_at, str):
            normalized_value: str = published_at.replace("Z", "+00:00")
            try:
                parsed_value: datetime = datetime.fromisoformat(normalized_value)
            except ValueError:
                return datetime.now(timezone.utc)
            if parsed_value.tzinfo is None:
                return parsed_value.replace(tzinfo=timezone.utc)
            return parsed_value
        return datetime.now(timezone.utc)
