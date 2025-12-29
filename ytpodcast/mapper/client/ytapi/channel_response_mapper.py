"""Module for ytpodcast.mapper.client.ytapi.channel_response_mapper."""

from typing import Any

from pyyoutube.models.channel import ChannelListResponse

from ytpodcast.model.client.ytapi.channel_response import ChannelResponse


# pylint: disable=too-few-public-methods
class ChannelResponseMapper:
    """Build ChannelResponse instances from YouTube API payloads."""

    def create_from_channel_list_response(
        self,
        response: ChannelListResponse,
        identifier: str,
    ) -> ChannelResponse:
        """Convert a channel list response into a ChannelResponse."""
        items: list[Any] = response.items
        if not items:
            raise ValueError(f"Channel not found for identifier '{identifier}'.")

        item = items[0]
        snippet = item.snippet
        channel_id: str = item.id or identifier
        image_url: str = self._resolve_thumbnail_url(getattr(snippet, "thumbnails", None))
        return ChannelResponse(
            channel_id=channel_id,
            title=snippet.title or "",
            description=snippet.description or "",
            url=f"https://www.youtube.com/channel/{channel_id}",
            image_url=image_url,
        )

    def _resolve_thumbnail_url(self, thumbnails: Any) -> str:
        """Return the best available thumbnail URL."""
        if thumbnails is None:
            return ""

        for key in ("high", "medium", "default"):
            thumbnail = getattr(thumbnails, key, None)
            if thumbnail is not None and getattr(thumbnail, "url", None):
                return thumbnail.url

        if isinstance(thumbnails, dict):
            for key in ("high", "medium", "default"):
                thumbnail = thumbnails.get(key)
                if thumbnail is None:
                    continue
                if isinstance(thumbnail, dict) and thumbnail.get("url"):
                    return str(thumbnail["url"])
                if getattr(thumbnail, "url", None):
                    return str(thumbnail.url)

        return ""
