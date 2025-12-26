"""Module for ytpodcast.model.client.ytapi.channel_videos_page_response."""

from pydantic import BaseModel

from ytpodcast.model.client.ytapi.channel_video_response import ChannelVideoResponse


class ChannelVideosPageResponse(BaseModel):
    """Client payload for paged channel video responses."""

    items: list[ChannelVideoResponse]
    next_page_token: str | None
