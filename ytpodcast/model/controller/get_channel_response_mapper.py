"""Module for ytpodcast.model.controller.get_channel_response_mapper."""

from ytpodcast.model.controller.get_channel_response import GetChannelResponse
from ytpodcast.model.service.channel import Channel


# pylint: disable=too-few-public-methods
class GetChannelResponseMapper:
    """Build channel response payloads from service models."""

    def create_from_channel(self, payload: Channel) -> GetChannelResponse:
        """Convert a service channel into a response payload."""
        return GetChannelResponse(**payload.dict())
