"""Module for ytpodcast.model.client.ytapi.channel_video_response."""

from datetime import datetime

from pydantic import BaseModel


class ChannelVideoResponse(BaseModel):
    """Client payload for a channel video entry."""

    video_id: str
    title: str
    description: str
    url: str
    published_at: datetime
