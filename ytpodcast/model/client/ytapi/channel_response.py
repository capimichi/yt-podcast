"""Module for ytpodcast.model.client.ytapi.channel_response."""

from pydantic import BaseModel


class ChannelResponse(BaseModel):
    """Channel payload from the YouTube API."""

    channel_id: str
    title: str
    description: str
    url: str
    image_url: str
    uploads_playlist_id: str | None = None

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

    def get_uploads_playlist_id(self) -> str | None:
        """Return the uploads playlist identifier."""
        return self.uploads_playlist_id
