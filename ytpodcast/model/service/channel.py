"""Module for ytpodcast.model.service.channel."""

from pydantic import BaseModel


class Channel(BaseModel):
    """Domain model for a YouTube channel."""

    channel_id: str
    title: str
    description: str
    url: str
    image_url: str

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

    def get_image_url(self) -> str:
        """Return the channel image URL."""
        return self.image_url
