from pydantic import BaseModel


class YtApiVideoModel(BaseModel):
    """Video payload from the YouTube API."""

    video_id: str
    title: str
    description: str
    duration_seconds: int
    url: str
    channel_id: str
