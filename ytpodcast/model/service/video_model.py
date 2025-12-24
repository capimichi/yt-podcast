from pydantic import BaseModel


class VideoModel(BaseModel):
    """Domain model for a YouTube video."""

    video_id: str
    title: str
    description: str
    duration_seconds: int
    url: str
    channel_id: str
    audio_format: str
    audio_bitrate_kbps: int | None
