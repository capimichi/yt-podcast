from ytpodcast.model.client.ytapi.video_model import YtApiVideoModel
from ytpodcast.model.service.video_model import VideoModel


class YtApiVideoModelToServiceVideoModelMapper:
    """Map YouTube API video model into the service video model."""

    def to_model(
        self,
        payload: YtApiVideoModel,
        audio_format: str,
        audio_bitrate_kbps: int | None,
    ) -> VideoModel:
        return VideoModel(
            video_id=payload.video_id,
            title=payload.title,
            description=payload.description,
            duration_seconds=payload.duration_seconds,
            url=payload.url,
            channel_id=payload.channel_id,
            audio_format=audio_format,
            audio_bitrate_kbps=audio_bitrate_kbps,
        )
