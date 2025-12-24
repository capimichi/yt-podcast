from ytpodcast.model.client.ytdl.format_model import YtDlAudioFormatModel


class YtDlClient:
    """Client wrapper around yt-dlp (stubbed)."""

    def __init__(self, default_format: str) -> None:
        self.default_format = default_format

    def fetch_audio_format(self, video_id: str) -> YtDlAudioFormatModel:
        return YtDlAudioFormatModel(
            format_id=self.default_format,
            extension="mp3",
            audio_bitrate_kbps=192,
            note=f"Default audio format for {video_id}",
        )
