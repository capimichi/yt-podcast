"""Module for ytpodcast.model.video_base."""

from pydantic import BaseModel


class VideoBase(BaseModel):
    """Shared fields for video payloads."""

    video_id: str
    title: str
    description: str
    duration_seconds: int
    url: str
    channel_id: str


class VideoAudio(VideoBase):
    """Video payload with audio details."""

    audio_format: str
    audio_bitrate_kbps: int | None
