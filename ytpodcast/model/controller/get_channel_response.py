"""Module for ytpodcast.model.controller.get_channel_response."""

from pydantic import BaseModel


class GetChannelResponse(BaseModel):
    """Response payload for channel routes."""

    channel_id: str
    title: str
    description: str
    url: str

    def get_channel_id(self) -> str:
        """Return the channel identifier."""
        return self.channel_id

    def get_title(self) -> str:
        """Return the channel title."""
        return self.title

    def get_description(self) -> str:
        """Return the channel description."""
        return self.description

    def get_url(self) -> str:
        """Return the channel URL."""
        return self.url
