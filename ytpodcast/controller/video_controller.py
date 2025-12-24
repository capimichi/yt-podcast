"""Module for ytpodcast.controller.video_controller."""

from fastapi import APIRouter
from fastapi.responses import Response
from injector import inject

from ytpodcast.model.controller.get_video_response_mapper import GetVideoResponseMapper
from ytpodcast.model.controller.get_video_response import GetVideoResponse
from ytpodcast.model.controller.xml_response_mapper import XmlResponseMapper
from ytpodcast.service.video_service import VideoService


# pylint: disable=too-few-public-methods
class VideoController:
    """Video API routes."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        video_service: VideoService,
        service_to_controller_mapper: GetVideoResponseMapper,
        controller_to_xml_mapper: XmlResponseMapper,
    ) -> None:
        """Wire dependencies and register routes."""
        self.video_service = video_service
        self.service_to_controller_mapper = service_to_controller_mapper
        self.controller_to_xml_mapper = controller_to_xml_mapper
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
            "/{video_id}/xml",
            self.get_video_xml,
            methods=["GET"],
            summary="Fetch video information as XML",
        )

    async def get_video(
        self,
        video_id: str,
    ) -> GetVideoResponse:
        """Return a video response in JSON."""
        service_model = self.video_service.get_video(video_id)
        return self.service_to_controller_mapper.create_from_video(service_model)

    async def get_video_xml(self, video_id: str) -> Response:
        """Return a video response in XML."""
        service_model = self.video_service.get_video(video_id)
        response_model = self.service_to_controller_mapper.create_from_video(service_model)
        xml_body = self.controller_to_xml_mapper.create_from_response("video", response_model)
        return Response(content=xml_body, media_type="application/xml")
