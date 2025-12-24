from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from injector import inject

from ytpodcast.model.controller.channel_response_mapper import ChannelResponseMapper
from ytpodcast.model.controller.xml_response_mapper import XmlResponseMapper
from ytpodcast.model.controller.channel_model import ChannelResponseModel
from ytpodcast.service.channel_service import ChannelService


class ChannelController:
    """Channel API routes."""

    @inject
    def __init__(
        self,
        channel_service: ChannelService,
        service_to_controller_mapper: ChannelResponseMapper,
        controller_to_xml_mapper: XmlResponseMapper,
    ) -> None:
        self.channel_service = channel_service
        self.service_to_controller_mapper = service_to_controller_mapper
        self.controller_to_xml_mapper = controller_to_xml_mapper
        self.router = APIRouter(prefix="/channels", tags=["Channels"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/{identifier}",
            self.get_channel,
            methods=["GET"],
            summary="Fetch channel information",
            response_model=ChannelResponseModel,
        )

    async def get_channel(
        self,
        identifier: str,
        response_format: str = Query("json", alias="format"),
    ) -> ChannelResponseModel | Response:
        if response_format not in {"json", "xml"}:
            raise HTTPException(status_code=400, detail="format must be json or xml")

        service_model = self.channel_service.get_channel(identifier)
        response_model = self.service_to_controller_mapper.create_from_channel(service_model)

        if response_format == "xml":
            xml_body = self.controller_to_xml_mapper.create_from_response("channel", response_model)
            return Response(content=xml_body, media_type="application/xml")

        return response_model
