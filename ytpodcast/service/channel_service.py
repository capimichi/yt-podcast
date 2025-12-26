"""Module for ytpodcast.service.channel_service."""

from injector import inject

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.mapper.service.channel_mapper import ChannelMapper
from ytpodcast.model.service.channel import Channel
from ytpodcast.model.client.ytapi.channel_response import ChannelResponse


# pylint: disable=too-few-public-methods
class ChannelService:
    """Service layer for channel data."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        yt_api_client: YtApiClient,
        yt_api_mapper: ChannelMapper,
    ) -> None:
        """Store dependencies for channel operations."""
        self.yt_api_client = yt_api_client
        self.yt_api_mapper = yt_api_mapper

    def get_channel(self, identifier: str) -> Channel:
        """Fetch and map channel data by identifier."""
        channel_response: ChannelResponse = self.yt_api_client.fetch_channel(identifier)
        return self.yt_api_mapper.create_from_channel_response(channel_response)
