"""Module for ytpodcast.model.client.ytapi.channel_response."""

from pydantic import BaseModel


class ChannelResponse(BaseModel):
    """Channel payload from the YouTube API."""

    channel_id: str
    title: str
    description: str
    url: str
