"""Module for ytpodcast.client.yt_dl_client."""

from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse


# pylint: disable=too-few-public-methods
class YtDlClient:
    """Client wrapper around yt-dlp (stubbed)."""

    def __init__(self, default_format: str) -> None:
        """Store default audio format settings."""
        self.default_format = default_format

    def fetch_audio_format(self, video_id: str) -> AudioFormatResponse:
        """Return a stubbed audio format payload."""
        return AudioFormatResponse(
            format_id=self.default_format,
            extension="mp3",
            audio_bitrate_kbps=192,
            note=f"Default audio format for {video_id}",
        )
