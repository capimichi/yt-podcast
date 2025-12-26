"""Module for ytpodcast.model.service.channel_feed."""

from pydantic import BaseModel

from ytpodcast.model.service.feed_item import FeedItem


class ChannelFeed(BaseModel):
    """Domain model for a channel feed."""

    channel_id: str
    title: str
    description: str
    url: str
    items: list[FeedItem]
