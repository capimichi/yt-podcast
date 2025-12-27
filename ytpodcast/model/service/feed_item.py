"""Module for ytpodcast.model.service.feed_item."""

from datetime import datetime

from pydantic import BaseModel


class FeedItem(BaseModel):
    """Domain model for a feed item."""

    video_id: str
    title: str
    description: str
    url: str
    published_at: datetime

    def get_video_id(self) -> str:
        """Return the video identifier."""
        return self.video_id

    def get_title(self) -> str:
        """Return the feed item title."""
        return self.title

    def get_description(self) -> str:
        """Return the feed item description."""
        return self.description

    def get_url(self) -> str:
        """Return the feed item URL."""
        return self.url

    def get_published_at(self) -> datetime:
        """Return the published timestamp."""
        return self.published_at
