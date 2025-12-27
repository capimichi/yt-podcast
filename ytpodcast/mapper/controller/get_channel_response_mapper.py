"""Module for ytpodcast.mapper.controller.get_channel_response_mapper."""

from ytpodcast.model.controller.get_channel_response import GetChannelResponse
from ytpodcast.model.service.channel import Channel


# pylint: disable=too-few-public-methods
class GetChannelResponseMapper:
    """Build channel response payloads from service models."""

    def create_from_channel(self, channel: Channel) -> GetChannelResponse:
        """Convert a service channel into a response payload."""
        return GetChannelResponse(
            channel_id=channel.get_channel_id(),
            title=channel.get_title(),
            description=channel.get_description(),
            url=channel.get_url(),
        )
