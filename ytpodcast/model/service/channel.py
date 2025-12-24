"""Module for ytpodcast.model.service.channel."""

from pydantic import BaseModel


class Channel(BaseModel):
    """Domain model for a YouTube channel."""

    channel_id: str
    title: str
    description: str
    url: str
