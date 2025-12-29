"""Module for ytpodcast.model.service.channel_feed."""

from pydantic import BaseModel

from ytpodcast.model.service.feed_item import FeedItem


class ChannelFeed(BaseModel):
    """Domain model for a channel feed."""

    channel_id: str
    title: str
    description: str
    url: str
    author: str
    image_url: str
    items: list[FeedItem]

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

    def get_author(self) -> str:
        """Return the channel author."""
        return self.author

    def get_image_url(self) -> str:
        """Return the channel image URL."""
        return self.image_url

    def get_items(self) -> list[FeedItem]:
        """Return the feed items."""
        return self.items
