"""Module for ytpodcast.mapper.controller.get_video_response_mapper."""

from ytpodcast.model.controller.get_video_response import GetVideoResponse
from ytpodcast.model.service.video import Video


# pylint: disable=too-few-public-methods
class GetVideoResponseMapper:
    """Build video response payloads from service models."""

    def create_from_video(self, video: Video) -> GetVideoResponse:
        """Convert a service video into a response payload."""
        return GetVideoResponse(
            video_id=video.get_video_id(),
            title=video.get_title(),
            description=video.get_description(),
            duration_seconds=video.get_duration_seconds(),
            url=video.get_url(),
            channel_id=video.get_channel_id(),
            audio_format=video.get_audio_format(),
            audio_bitrate_kbps=video.get_audio_bitrate_kbps(),
        )
