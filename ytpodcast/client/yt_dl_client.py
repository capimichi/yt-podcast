"""Module for ytpodcast.client.yt_dl_client."""

from pathlib import Path
from typing import Any

import yt_dlp

from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse


# pylint: disable=too-few-public-methods
class YtDlClient:
    """Client wrapper around yt-dlp."""

    def __init__(self, default_format: str, download_dir: str) -> None:
        """Store default audio format settings."""
        self.default_format = default_format
        self.download_dir = download_dir

    def fetch_audio_format(self, video_id: str) -> AudioFormatResponse:
        """Return a default audio format payload."""
        return AudioFormatResponse(
            format_id=self.default_format,
            extension="mp3",
            audio_bitrate_kbps=192,
            is_audio_only=True,
            note=f"Default audio format for {video_id}",
        )

    def fetch_audio_formats(self, video_id: str) -> list[AudioFormatResponse]:
        """Return available audio formats for a video."""
        info: dict[str, Any] = self._extract_info(video_id)
        formats: list[dict[str, Any]] = info.get("formats", [])
        audio_formats: list[AudioFormatResponse] = []
        for format_payload in formats:
            format_id: str | None = format_payload.get("format_id")
            if not format_id:
                continue
            audio_codec: str | None = format_payload.get("acodec")
            if not audio_codec or audio_codec == "none":
                continue
            video_codec: str | None = format_payload.get("vcodec")
            is_audio_only: bool = video_codec in (None, "none")
            extension: str = format_payload.get("ext") or "mp3"
            bitrate: float | int | None = format_payload.get("abr") or format_payload.get("tbr")
            audio_bitrate_kbps: int | None = None
            if isinstance(bitrate, (int, float)):
                audio_bitrate_kbps = int(bitrate)
            note: str | None = format_payload.get("format_note")
            audio_formats.append(
                AudioFormatResponse(
                    format_id=str(format_id),
                    extension=extension,
                    audio_bitrate_kbps=audio_bitrate_kbps,
                    is_audio_only=is_audio_only,
                    note=note,
                )
            )
        return audio_formats

    def download_audio(self, video_id: str) -> Path:
        """Download a single audio format for a video."""
        download_dir_path: Path = Path(self.download_dir)
        download_dir_path.mkdir(parents=True, exist_ok=True)
        existing_files: list[Path] = list(download_dir_path.glob(f"{video_id}.*"))
        if existing_files:
            return existing_files[0]
        audio_formats: list[AudioFormatResponse] = self.fetch_audio_formats(video_id)
        selected_format: AudioFormatResponse = self._select_best_audio_format(audio_formats)
        output_path: Path = download_dir_path / f"{video_id}.{selected_format.extension}"
        options: dict[str, Any] = {
            "format": selected_format.format_id,
            "outtmpl": str(output_path),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([self._build_video_url(video_id)])
        return output_path

    def _select_best_audio_format(
        self,
        audio_formats: list[AudioFormatResponse],
    ) -> AudioFormatResponse:
        """Pick the best available audio format."""
        if not audio_formats:
            raise ValueError("No audio formats available for download.")
        audio_only: list[AudioFormatResponse] = [
            format_item for format_item in audio_formats if format_item.is_audio_only
        ]
        candidates: list[AudioFormatResponse] = audio_only or audio_formats
        return max(
            candidates,
            key=lambda format_item: format_item.audio_bitrate_kbps or 0,
        )

    def _extract_info(self, video_id: str) -> dict[str, Any]:
        """Extract metadata from a video without downloading."""
        options: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(self._build_video_url(video_id), download=False)

    def _build_video_url(self, video_id: str) -> str:
        """Build a YouTube watch URL for a video."""
        return f"https://www.youtube.com/watch?v={video_id}"
