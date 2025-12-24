"""Module for ytpodcast.service.video_service."""

from injector import inject

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.client.yt_dl_client import YtDlClient
from ytpodcast.model.service.video_mapper import VideoMapper
from ytpodcast.model.service.video import Video


# pylint: disable=too-few-public-methods
class VideoService:
    """Service layer for video data."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        yt_api_client: YtApiClient,
        yt_dl_client: YtDlClient,
        video_mapper: VideoMapper,
    ) -> None:
        """Store dependencies for video operations."""
        self.yt_api_client = yt_api_client
        self.yt_dl_client = yt_dl_client
        self.video_mapper = video_mapper

    def get_video(self, video_id: str) -> Video:
        """Fetch and map video data by id."""
        yt_api_payload = self.yt_api_client.fetch_video(video_id)
        yt_dl_payload = self.yt_dl_client.fetch_audio_format(video_id)
        return self.video_mapper.create_from_video_response(yt_api_payload, yt_dl_payload)
