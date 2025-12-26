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
