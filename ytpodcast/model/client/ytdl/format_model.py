from pydantic import BaseModel


class YtDlAudioFormatModel(BaseModel):
    """Audio format details returned by yt-dlp."""

    format_id: str
    extension: str
    audio_bitrate_kbps: int | None
    note: str | None = None
