"""Module for ytpodcast.controller.video_controller."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse
from injector import inject

from ytpodcast.mapper.controller.file_response_mapper import FileResponseMapper
from ytpodcast.mapper.controller.get_video_response_mapper import GetVideoResponseMapper
from ytpodcast.model.controller.get_video_response import GetVideoResponse
from ytpodcast.service.video_service import VideoService


# pylint: disable=too-few-public-methods
class VideoController:
    """Video API routes."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        video_service: VideoService,
        service_to_controller_mapper: GetVideoResponseMapper,
        file_response_mapper: FileResponseMapper,
    ) -> None:
        """Wire dependencies and register routes."""
        self.video_service = video_service
        self.service_to_controller_mapper = service_to_controller_mapper
        self.file_response_mapper = file_response_mapper
        self.router = APIRouter(prefix="/videos", tags=["Videos"])
        self._register_routes()

    def _register_routes(self) -> None:
        """Register FastAPI routes for videos."""
        self.router.add_api_route(
            "/{video_id}",
            self.get_video,
            methods=["GET"],
            summary="Fetch video information",
            response_model=GetVideoResponse,
        )
        self.router.add_api_route(
            "/{video_id}/download",
            self.download_video,
            methods=["GET"],
            summary="Download video audio",
        )

    async def get_video(
        self,
        video_id: str,
    ) -> GetVideoResponse:
        """Return a video response in JSON."""
        service_model = self.video_service.get_video(video_id)
        return self.service_to_controller_mapper.create_from_video(service_model)

    async def download_video(self, video_id: str) -> FileResponse:
        """Download a single audio file for a video."""
        download_path: Path = self.video_service.download_audio(video_id)
        return self.file_response_mapper.create_from_path(download_path)
