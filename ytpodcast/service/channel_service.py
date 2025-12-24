from injector import inject

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.model.service.channel_mapper import ChannelMapper
from ytpodcast.model.service.channel_model import ChannelModel


class ChannelService:
    """Service layer for channel data."""

    @inject
    def __init__(
        self,
        yt_api_client: YtApiClient,
        yt_api_mapper: ChannelMapper,
    ) -> None:
        self.yt_api_client = yt_api_client
        self.yt_api_mapper = yt_api_mapper

    def get_channel(self, identifier: str) -> ChannelModel:
        payload = self.yt_api_client.fetch_channel(identifier)
        return self.yt_api_mapper.create_from_ytapi(payload)
