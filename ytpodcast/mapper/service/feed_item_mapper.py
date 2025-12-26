"""Module for ytpodcast.mapper.service.feed_item_mapper."""

from ytpodcast.model.client.ytapi.channel_video_response import ChannelVideoResponse
from ytpodcast.model.service.feed_item import FeedItem


# pylint: disable=too-few-public-methods
class FeedItemMapper:
    """Build feed items from YouTube API payloads."""

    def create_from_channel_video_response(
        self,
        channel_video_response: ChannelVideoResponse,
    ) -> FeedItem:
        """Convert a channel video payload into a feed item."""
        return FeedItem(
            video_id=channel_video_response.video_id,
            title=channel_video_response.title,
            description=channel_video_response.description,
            url=channel_video_response.url,
            published_at=channel_video_response.published_at,
        )
