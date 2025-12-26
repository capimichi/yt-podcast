"""Module for ytpodcast.model.controller.get_video_response_mapper."""

from ytpodcast.model.controller.get_video_response import GetVideoResponse
from ytpodcast.model.service.video import Video


# pylint: disable=too-few-public-methods
class GetVideoResponseMapper:
    """Build video response payloads from service models."""

    def create_from_video(self, video: Video) -> GetVideoResponse:
        """Convert a service video into a response payload."""
        return GetVideoResponse(**video.dict())
