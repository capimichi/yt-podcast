"""Module for ytpodcast.service.feed_service."""

from datetime import datetime
from datetime import timezone

from injector import inject

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.model.client.ytapi.channel_response import ChannelResponse
from ytpodcast.model.client.ytapi.channel_video_response import ChannelVideoResponse
from ytpodcast.model.client.ytapi.channel_videos_page_response import ChannelVideosPageResponse
from ytpodcast.model.service.channel import Channel
from ytpodcast.model.service.channel_feed import ChannelFeed
from ytpodcast.mapper.service.channel_mapper import ChannelMapper
from ytpodcast.model.service.feed_item import FeedItem
from ytpodcast.mapper.service.feed_item_mapper import FeedItemMapper


# pylint: disable=too-few-public-methods
class FeedService:
    """Service layer for channel feeds."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(
        self,
        yt_api_client: YtApiClient,
        channel_mapper: ChannelMapper,
        feed_item_mapper: FeedItemMapper,
    ) -> None:
        """Store dependencies for feed operations."""
        self.yt_api_client = yt_api_client
        self.channel_mapper = channel_mapper
        self.feed_item_mapper = feed_item_mapper

    def get_channel_feed(
        self,
        channel_id: str,
        limit: int | None = None,
        offset: int | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        include_shorts: bool = True,
    ) -> ChannelFeed:
        """Fetch channel metadata and recent videos for feed rendering."""
        channel_response: ChannelResponse = self.yt_api_client.fetch_channel(channel_id)
        channel: Channel = self.channel_mapper.create_from_channel_response(channel_response)
        requested_total: int = self._resolve_requested_total(limit, offset)
        filtered_responses: list[ChannelVideoResponse] = self._collect_filtered_videos(
            channel.get_channel_id(),
            requested_total,
            from_date,
            to_date,
            include_shorts,
        )
        sliced_responses: list[ChannelVideoResponse] = self._apply_paging(
            filtered_responses,
            limit,
            offset,
        )
        items: list[FeedItem] = [
            self.feed_item_mapper.create_from_channel_video_response(video_response)
            for video_response in sliced_responses
        ]
        return ChannelFeed(
            channel_id=channel.get_channel_id(),
            title=channel.get_title(),
            description=channel.get_description(),
            url=channel.get_url(),
            author=channel.get_title(),
            image_url=channel.get_image_url(),
            items=items,
        )

    def _resolve_requested_total(self, limit: int | None, offset: int | None) -> int:
        """Determine how many items to collect before paging."""
        default_limit: int = 20
        if limit is None and offset is None:
            return default_limit
        offset_value: int = offset or 0
        requested_total: int = offset_value + (limit or default_limit)
        return max(requested_total, 1)

    def _collect_filtered_videos(
        self,
        channel_id: str,
        requested_total: int,
        from_date: datetime | None,
        to_date: datetime | None,
        include_shorts: bool,
    ) -> list[ChannelVideoResponse]:
        """Fetch paged videos until enough filtered items are collected."""
        collected: list[ChannelVideoResponse] = []
        seen_video_ids: set[str] = set()
        page_token: str | None = None

        while len(collected) < requested_total:
            remaining: int = requested_total - len(collected)
            page_size: int = min(max(remaining, 1), 50)
            page: ChannelVideosPageResponse = self.yt_api_client.fetch_channel_videos_page(
                channel_id,
                max_results=page_size,
                page_token=page_token,
            )
            page_filtered: list[ChannelVideoResponse] = self._filter_by_date_range(
                page.get_items(),
                from_date,
                to_date,
            )
            for video in page_filtered:
                video_id: str = video.get_video_id()
                if video_id in seen_video_ids:
                    continue
                if not include_shorts and self._is_short_video(video_id):
                    continue
                seen_video_ids.add(video_id)
                collected.append(video)
            if not page.get_next_page_token():
                break
            page_token = page.get_next_page_token()
        return collected

    def _is_short_video(self, video_id: str) -> bool:
        """Return True when the video is a YouTube Short."""
        max_shorts_seconds: int = 60
        try:
            video_response = self.yt_api_client.fetch_video(video_id)
        except ValueError:
            return False
        return video_response.get_duration_seconds() <= max_shorts_seconds

    def _normalize_filter_date(self, value: datetime | None) -> datetime | None:
        """Normalize filter dates to UTC-aware values."""
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    def _filter_by_date_range(
        self,
        video_responses: list[ChannelVideoResponse],
        from_date: datetime | None,
        to_date: datetime | None,
    ) -> list[ChannelVideoResponse]:
        """Filter channel videos by published date range."""
        normalized_from: datetime | None = self._normalize_filter_date(from_date)
        normalized_to: datetime | None = self._normalize_filter_date(to_date)
        filtered: list[ChannelVideoResponse] = []
        for video in video_responses:
            published_at: datetime = video.get_published_at()
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            published_at = published_at.astimezone(timezone.utc)
            if normalized_from and published_at < normalized_from:
                continue
            if normalized_to and published_at > normalized_to:
                continue
            filtered.append(video)
        return filtered

    def _apply_paging(
        self,
        video_responses: list[ChannelVideoResponse],
        limit: int | None,
        offset: int | None,
    ) -> list[ChannelVideoResponse]:
        """Apply offset/limit to the filtered responses."""
        offset_value: int = offset or 0
        if offset_value >= len(video_responses):
            return []
        if limit is None:
            return video_responses[offset_value:]
        return video_responses[offset_value : offset_value + limit]
