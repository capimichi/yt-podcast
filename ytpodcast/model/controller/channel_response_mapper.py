from ytpodcast.model.controller.channel_model import ChannelResponseModel
from ytpodcast.model.service.channel_model import ChannelModel


class ChannelResponseMapper:
    """Build ChannelResponseModel instances from service models."""

    def create_from_channel(self, payload: ChannelModel) -> ChannelResponseModel:
        return ChannelResponseModel(**payload.dict())
