from ytpodcast.model.client.ytapi.channel_model import YtApiChannelModel
from ytpodcast.model.service.channel_model import ChannelModel


class YtApiChannelModelToServiceChannelModelMapper:
    """Map YouTube API channel model into the service channel model."""

    def to_model(self, payload: YtApiChannelModel) -> ChannelModel:
        return ChannelModel(
            channel_id=payload.channel_id,
            title=payload.title,
            description=payload.description,
            url=payload.url,
        )
