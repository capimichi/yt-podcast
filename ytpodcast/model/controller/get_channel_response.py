"""Module for ytpodcast.model.controller.get_channel_response."""

from pydantic import BaseModel


class GetChannelResponse(BaseModel):
    """Response payload for channel routes."""

    channel_id: str
    title: str
    description: str
    url: str
