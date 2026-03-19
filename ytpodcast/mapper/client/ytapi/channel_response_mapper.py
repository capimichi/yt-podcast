"""Module for ytpodcast.mapper.client.ytapi.channel_response_mapper."""

from typing import Any, cast

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
        uploads_playlist_id: str | None = self._resolve_uploads_playlist_id(item)
        return ChannelResponse(
            channel_id=channel_id,
            title=snippet.title or "",
            description=snippet.description or "",
            url=f"https://www.youtube.com/channel/{channel_id}",
            image_url=image_url,
            uploads_playlist_id=uploads_playlist_id,
        )

    def _resolve_uploads_playlist_id(self, item: Any) -> str | None:
        """Return the uploads playlist identifier when available."""
        content_details = getattr(item, "contentDetails", None)
        if content_details is None:
            return None

        related_playlists = getattr(content_details, "relatedPlaylists", None)
        if related_playlists is None:
            return None

        uploads_playlist_id: str | None = getattr(related_playlists, "uploads", None)
        return uploads_playlist_id or None

    def _resolve_thumbnail_url(self, thumbnails: Any) -> str:
        """Return the best available thumbnail URL."""
        if thumbnails is None:
            return ""

        for key in ("high", "medium", "default"):
            thumbnail = getattr(thumbnails, key, None)
            thumbnail_url: Any = getattr(thumbnail, "url", None)
            if thumbnail_url:
                return cast(str, thumbnail_url)

        if isinstance(thumbnails, dict):
            thumbnails_dict: dict[str, Any] = thumbnails
            for key in ("high", "medium", "default"):
                thumbnail: Any = thumbnails_dict.get(key)
                if thumbnail is None:
                    continue
                if isinstance(thumbnail, dict):
                    thumbnail_url: Any = thumbnail.get("url")
                    if thumbnail_url:
                        return cast(str, thumbnail_url)

        return ""
