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

    def get_video_id(self) -> str:
        """Return the video identifier."""
        return self.video_id

    def get_title(self) -> str:
        """Return the video title."""
        return self.title

    def get_description(self) -> str:
        """Return the video description."""
        return self.description

    def get_duration_seconds(self) -> int:
        """Return the video duration in seconds."""
        return self.duration_seconds

    def get_url(self) -> str:
        """Return the video URL."""
        return self.url

    def get_channel_id(self) -> str:
        """Return the channel identifier."""
        return self.channel_id


class VideoAudio(VideoBase):
    """Video payload with audio details."""

    audio_format: str
    audio_bitrate_kbps: int | None

    def get_audio_format(self) -> str:
        """Return the audio format identifier."""
        return self.audio_format

    def get_audio_bitrate_kbps(self) -> int | None:
        """Return the audio bitrate in kbps, if available."""
        return self.audio_bitrate_kbps
