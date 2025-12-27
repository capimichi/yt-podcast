"""Module for ytpodcast.mapper.service.channel_mapper."""

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.service.channel import Channel


# pylint: disable=too-few-public-methods
class ChannelMapper:
    """Build channel domain instances from client payloads."""

    def create_from_channel_response(self, channel_response: ChannelResponse) -> Channel:
        """Convert a YouTube API payload into a channel."""
        return Channel(
            channel_id=channel_response.get_channel_id(),
            title=channel_response.get_title(),
            description=channel_response.get_description(),
            url=channel_response.get_url(),
        )
