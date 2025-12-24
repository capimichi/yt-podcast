from ytpodcast.model.client.ytapi.video_model import YtApiVideoModel
from ytpodcast.model.client.ytdl.format_model import YtDlAudioFormatModel
from ytpodcast.model.service.video_model import VideoModel


class VideoMapper:
    """Build VideoModel instances from client payloads."""

    def create_from_ytdl(
        self,
        ytapi_payload: YtApiVideoModel,
        ytdl_payload: YtDlAudioFormatModel,
    ) -> VideoModel:
        return VideoModel(
            video_id=ytapi_payload.video_id,
            title=ytapi_payload.title,
            description=ytapi_payload.description,
            duration_seconds=ytapi_payload.duration_seconds,
            url=ytapi_payload.url,
            channel_id=ytapi_payload.channel_id,
            audio_format=ytdl_payload.format_id,
            audio_bitrate_kbps=ytdl_payload.audio_bitrate_kbps,
        )
