from ytpodcast.model.controller.channel_model import ChannelResponseModel
from ytpodcast.model.service.channel_model import ChannelModel


class ServiceChannelModelToControllerChannelModelMapper:
    """Map service channel model into controller channel model."""

    def to_model(self, payload: ChannelModel) -> ChannelResponseModel:
        return ChannelResponseModel(**payload.dict())
