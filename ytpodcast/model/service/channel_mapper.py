"""Module for ytpodcast.model.service.channel_mapper."""

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.service.channel import Channel


# pylint: disable=too-few-public-methods
class ChannelMapper:
    """Build channel domain instances from client payloads."""

    def create_from_channel_response(self, payload: ChannelResponse) -> Channel:
        """Convert a YouTube API payload into a channel."""
        return Channel(
            channel_id=payload.channel_id,
            title=payload.title,
            description=payload.description,
            url=payload.url,
        )
