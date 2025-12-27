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

    def get_format_id(self) -> str:
        """Return the format id for the audio payload."""
        return self.format_id

    def get_extension(self) -> str:
        """Return the file extension for the audio payload."""
        return self.extension

    def get_audio_bitrate_kbps(self) -> int | None:
        """Return the audio bitrate in kbps, if available."""
        return self.audio_bitrate_kbps

    def get_is_audio_only(self) -> bool:
        """Return whether the format is audio-only."""
        return self.is_audio_only

    def get_language(self) -> str | None:
        """Return the language tag for the format, if any."""
        return self.language

    def get_note(self) -> str | None:
        """Return the format note, if any."""
        return self.note
