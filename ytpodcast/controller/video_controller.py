from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from injector import inject

from ytpodcast.model.controller.video_response_mapper import VideoResponseMapper
from ytpodcast.model.controller.xml_response_mapper import XmlResponseMapper
from ytpodcast.model.controller.video_model import VideoResponseModel
from ytpodcast.service.video_service import VideoService


class VideoController:
    """Video API routes."""

    @inject
    def __init__(
        self,
        video_service: VideoService,
        service_to_controller_mapper: VideoResponseMapper,
        controller_to_xml_mapper: XmlResponseMapper,
    ) -> None:
        self.video_service = video_service
        self.service_to_controller_mapper = service_to_controller_mapper
        self.controller_to_xml_mapper = controller_to_xml_mapper
        self.router = APIRouter(prefix="/videos", tags=["Videos"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/{video_id}",
            self.get_video,
            methods=["GET"],
            summary="Fetch video information",
            response_model=VideoResponseModel,
        )

    async def get_video(
        self,
        video_id: str,
        response_format: str = Query("json", alias="format"),
    ) -> VideoResponseModel | Response:
        if response_format not in {"json", "xml"}:
            raise HTTPException(status_code=400, detail="format must be json or xml")

        service_model = self.video_service.get_video(video_id)
        response_model = self.service_to_controller_mapper.create_from_video(service_model)

        if response_format == "xml":
            xml_body = self.controller_to_xml_mapper.create_from_response("video", response_model)
            return Response(content=xml_body, media_type="application/xml")

        return response_model
