"""Module for ytpodcast.model.service.video_mapper."""

from ytpodcast.model.client.ytapi.video_response import VideoResponse
from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse
from ytpodcast.model.service.video import Video


# pylint: disable=too-few-public-methods
class VideoMapper:
    """Build video domain instances from client payloads."""

    def create_from_video_response(
        self,
        video_payload: VideoResponse,
        audio_payload: AudioFormatResponse,
    ) -> Video:
        """Combine API and yt-dlp payloads into a video."""
        return Video(
            video_id=video_payload.video_id,
            title=video_payload.title,
            description=video_payload.description,
            duration_seconds=video_payload.duration_seconds,
            url=video_payload.url,
            channel_id=video_payload.channel_id,
            audio_format=audio_payload.format_id,
            audio_bitrate_kbps=audio_payload.audio_bitrate_kbps,
        )
