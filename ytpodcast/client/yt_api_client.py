from ytpodcast.model.client.ytapi.channel_model import YtApiChannelModel
from ytpodcast.model.client.ytapi.video_model import YtApiVideoModel


class YtApiClient:
    """Client wrapper for the YouTube Data API (stubbed)."""

    def __init__(self, base_url: str, api_key: str | None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def fetch_channel(self, identifier: str) -> YtApiChannelModel:
        return YtApiChannelModel(
            channel_id=identifier,
            title=f"Channel {identifier}",
            description="Sample channel description",
            url=f"{self.base_url}/channels/{identifier}",
        )

    def fetch_video(self, video_id: str) -> YtApiVideoModel:
        return YtApiVideoModel(
            video_id=video_id,
            title=f"Video {video_id}",
            description="Sample video description",
            duration_seconds=0,
            url=f"{self.base_url}/videos/{video_id}",
            channel_id="sample-channel",
        )
