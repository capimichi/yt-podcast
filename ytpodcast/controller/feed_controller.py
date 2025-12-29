"""Module for ytpodcast.controller.feed_controller."""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Query
from fastapi.responses import Response
from injector import inject

from ytpodcast.manager.cache_manager import CacheManager
from ytpodcast.mapper.controller.rss_feed_response_mapper import RssFeedResponseMapper
from ytpodcast.model.service.channel_feed import ChannelFeed
from ytpodcast.service.feed_service import FeedService


# pylint: disable=too-few-public-methods
class FeedController:
    """Feed API routes."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        feed_service: FeedService,
        feed_response_mapper: RssFeedResponseMapper,
        cache_manager: CacheManager,
    ) -> None:
        """Wire dependencies and register routes."""
        self.feed_service = feed_service
        self.feed_response_mapper = feed_response_mapper
        self.cache_manager = cache_manager
        self.router = APIRouter(prefix="/feeds", tags=["Feeds"])
        self._register_routes()

    def _register_routes(self) -> None:
        """Register FastAPI routes for feeds."""
        self.router.add_api_route(
            "/{channel_id}/xml",
            self.get_feed_xml,
            methods=["GET"],
            summary="Fetch channel RSS feed as XML",
        )

    async def get_feed_xml(
        self,
        channel_id: str,
        limit: int | None = Query(default=None, ge=1),
        offset: int | None = Query(default=None, ge=0),
        from_date: datetime | None = Query(default=None, alias="fromDate"),
        to_date: datetime | None = Query(default=None, alias="toDate"),
        include_shorts: bool = Query(default=False, alias="includeShorts"),
    ) -> Response:
        """Return a channel feed response in RSS XML."""
        cache_key: str = self.cache_manager.create_cache_key(
            "feed_xml",
            channel_id,
            limit,
            offset,
            from_date,
            to_date,
            include_shorts,
        )
        cached_value: str | None = self.cache_manager.get(cache_key)
        if cached_value is not None:
            return Response(content=cached_value, media_type="application/rss+xml")

        feed: ChannelFeed = self.feed_service.get_channel_feed(
            channel_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
            include_shorts=include_shorts,
        )
        xml_body: str = self.feed_response_mapper.create_from_feed(feed)
        self.cache_manager.set(cache_key, xml_body, ttl_seconds=10800)
        return Response(content=xml_body, media_type="application/rss+xml")
