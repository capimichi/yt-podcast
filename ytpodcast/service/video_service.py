"""Module for ytpodcast.service.video_service."""

from pathlib import Path

from injector import inject

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.client.yt_dl_client import YtDlClient
from ytpodcast.model.client.ytapi.video_response import VideoResponse
from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse
from ytpodcast.mapper.service.video_mapper import VideoMapper
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
        yt_api_response: VideoResponse = self.yt_api_client.fetch_video(video_id)
        audio_format_response: AudioFormatResponse = self.yt_dl_client.fetch_audio_format(
            video_id
        )
        return self.video_mapper.create_from_video_response(
            yt_api_response,
            audio_format_response,
        )

    def download_audio(self, video_id: str) -> Path:
        """Download a single audio format for a video."""
        audio_formats: list[AudioFormatResponse] = self.yt_dl_client.fetch_audio_formats(
            video_id
        )
        selected_format: AudioFormatResponse = self._select_best_audio_format(audio_formats)
        return self.yt_dl_client.download_audio(
            video_id,
            selected_format.get_format_id(),
        )

    def _select_best_audio_format(
        self,
        audio_formats: list[AudioFormatResponse],
    ) -> AudioFormatResponse:
        """Pick the best available audio format."""
        if not audio_formats:
            raise ValueError("No audio formats available for download.")
        audio_only: list[AudioFormatResponse] = [
            format_item for format_item in audio_formats if format_item.get_is_audio_only()
        ]
        candidates: list[AudioFormatResponse] = audio_only or audio_formats
        italian_candidates: list[AudioFormatResponse] = [
            format_item
            for format_item in candidates
            if (format_item.get_language() or "").lower() == "it"
        ]
        return italian_candidates[0] if italian_candidates else candidates[0]
