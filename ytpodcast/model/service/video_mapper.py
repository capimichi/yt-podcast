"""Module for ytpodcast.model.service.video_mapper."""

from ytpodcast.model.client.ytapi.video_response import VideoResponse
from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse
from ytpodcast.model.service.video import Video


# pylint: disable=too-few-public-methods
class VideoMapper:
    """Build video domain instances from client payloads."""

    def create_from_video_response(
        self,
        video_response: VideoResponse,
        audio_format_response: AudioFormatResponse,
    ) -> Video:
        """Combine API and yt-dlp payloads into a video."""
        return Video(
            video_id=video_response.video_id,
            title=video_response.title,
            description=video_response.description,
            duration_seconds=video_response.duration_seconds,
            url=video_response.url,
            channel_id=video_response.channel_id,
            audio_format=audio_format_response.format_id,
            audio_bitrate_kbps=audio_format_response.audio_bitrate_kbps,
        )
