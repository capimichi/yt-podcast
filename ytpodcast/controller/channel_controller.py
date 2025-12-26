"""Module for ytpodcast.controller.channel_controller."""

from fastapi import APIRouter
from injector import inject

from ytpodcast.mapper.controller.get_channel_response_mapper import GetChannelResponseMapper
from ytpodcast.model.controller.get_channel_response import GetChannelResponse
from ytpodcast.service.channel_service import ChannelService


# pylint: disable=too-few-public-methods
class ChannelController:
    """Channel API routes."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        channel_service: ChannelService,
        service_to_controller_mapper: GetChannelResponseMapper,
    ) -> None:
        """Wire dependencies and register routes."""
        self.channel_service = channel_service
        self.service_to_controller_mapper = service_to_controller_mapper
        self.router = APIRouter(prefix="/channels", tags=["Channels"])
        self._register_routes()

    def _register_routes(self) -> None:
        """Register FastAPI routes for channels."""
        self.router.add_api_route(
            "/{identifier}",
            self.get_channel,
            methods=["GET"],
            summary="Fetch channel information",
            response_model=GetChannelResponse,
        )

    async def get_channel(
        self,
        identifier: str,
    ) -> GetChannelResponse:
        """Return a channel response in JSON."""
        service_model = self.channel_service.get_channel(identifier)
        return self.service_to_controller_mapper.create_from_channel(service_model)
