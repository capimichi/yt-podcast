"""Module for ytpodcast.model.client.ytdl.audio_format_response."""

from pydantic import BaseModel


class AudioFormatResponse(BaseModel):
    """Audio format details returned by yt-dlp."""

    format_id: str
    extension: str
    audio_bitrate_kbps: int | None
    is_audio_only: bool
    language: str | None = None
    note: str | None = None
