from ytpodcast.model.client.ytdl.format_model import YtDlAudioFormatModel


class YtDlAudioFormatModelToServiceAudioFormatMapper:
    """Map yt-dlp audio format model into service audio fields."""

    def to_model(self, payload: YtDlAudioFormatModel) -> tuple[str, int | None]:
        return payload.format_id, payload.audio_bitrate_kbps
