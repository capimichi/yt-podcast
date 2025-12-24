from ytpodcast.model.client.ytapi.channel_model import YtApiChannelModel
from ytpodcast.model.service.channel_model import ChannelModel


class ChannelMapper:
    """Build ChannelModel instances from client payloads."""

    def create_from_ytapi(self, payload: YtApiChannelModel) -> ChannelModel:
        return ChannelModel(
            channel_id=payload.channel_id,
            title=payload.title,
            description=payload.description,
            url=payload.url,
        )
