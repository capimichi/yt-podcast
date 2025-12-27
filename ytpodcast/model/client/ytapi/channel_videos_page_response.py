"""Module for ytpodcast.model.client.ytapi.channel_videos_page_response."""

from pydantic import BaseModel

from ytpodcast.model.client.ytapi.channel_video_response import ChannelVideoResponse


class ChannelVideosPageResponse(BaseModel):
    """Client payload for paged channel video responses."""

    items: list[ChannelVideoResponse]
    next_page_token: str | None

    def get_items(self) -> list[ChannelVideoResponse]:
        """Return the channel video items."""
        return self.items

    def get_next_page_token(self) -> str | None:
        """Return the next page token, if any."""
        return self.next_page_token
