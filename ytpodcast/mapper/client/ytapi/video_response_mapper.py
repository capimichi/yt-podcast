"""Module for ytpodcast.mapper.client.ytapi.video_response_mapper."""

from datetime import timedelta
from typing import Any

from isodate import parse_duration
from isodate.duration import Duration
from pyyoutube.models.video import VideoListResponse

from ytpodcast.model.client.ytapi.video_response import VideoResponse


# pylint: disable=too-few-public-methods
class VideoResponseMapper:
    """Build VideoResponse instances from YouTube API payloads."""

    def create_from_video_list_response(
        self,
        response: VideoListResponse,
        video_id: str,
    ) -> VideoResponse:
        """Convert a video list response into a VideoResponse."""
        items: list[Any] = response.items
        if not items:
            raise ValueError(f"Video not found for id '{video_id}'.")

        item = items[0]
        snippet = item.snippet
        content_details = item.contentDetails
        duration_seconds: int = self._parse_duration_seconds(content_details.duration)
        channel_id: str = snippet.channelId or ""
        return VideoResponse(
            video_id=item.id or video_id,
            title=snippet.title or "",
            description=snippet.description or "",
            duration_seconds=duration_seconds,
            url=f"https://www.youtube.com/watch?v={video_id}",
            channel_id=channel_id,
        )

    def _parse_duration_seconds(self, duration_value: str | None) -> int:
        """Return the duration in seconds for ISO8601 values."""
        duration_iso: str = duration_value or "PT0S"
        duration: timedelta | Duration = parse_duration(duration_iso)
        if isinstance(duration, timedelta):
            return int(duration.total_seconds())
        return 0
