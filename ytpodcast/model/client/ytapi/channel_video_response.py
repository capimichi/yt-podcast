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

    def get_video_id(self) -> str:
        """Return the video identifier."""
        return self.video_id

    def get_title(self) -> str:
        """Return the video title."""
        return self.title

    def get_description(self) -> str:
        """Return the video description."""
        return self.description

    def get_url(self) -> str:
        """Return the video URL."""
        return self.url

    def get_published_at(self) -> datetime:
        """Return the published timestamp."""
        return self.published_at
