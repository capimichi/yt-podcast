"""Module for ytpodcast.client.yt_dl_client."""

import json
import subprocess
from pathlib import Path
from typing import Any

from ytpodcast.model.client.ytdl.audio_format_response import AudioFormatResponse


# pylint: disable=too-few-public-methods
class YtDlClient:
    """Client wrapper around yt-dlp."""

    def __init__(
        self,
        default_format: str,
        download_dir: str,
        executable_path: str,
    ) -> None:
        """Store default audio format settings."""
        self.default_format = default_format
        self.download_dir = download_dir
        self.executable_path = executable_path

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
            resolution: str | None = format_payload.get("resolution")
            is_audio_only: bool = resolution == "audio only"
            extension: str = format_payload.get("ext") or "mp3"
            audio_bitrate_kbps: int | None = None
            language: str | None = format_payload.get("language")
            note: str | None = format_payload.get("format_note")
            audio_formats.append(
                AudioFormatResponse(
                    format_id=str(format_id),
                    extension=extension,
                    audio_bitrate_kbps=audio_bitrate_kbps,
                    is_audio_only=is_audio_only,
                    language=language,
                    note=note,
                )
            )
        return audio_formats

    def download_audio(self, video_id: str, format_id: str, extension: str) -> Path:
        """Download a single audio format for a video."""
        download_dir_path: Path = Path(self.download_dir)
        download_dir_path.mkdir(parents=True, exist_ok=True)
        output_path: Path = download_dir_path / f"{video_id}.{extension}"
        if output_path.exists():
            return output_path
        command: list[str] = [
            self.executable_path,
            "--no-playlist",
            "--quiet",
            "--no-warnings",
            "-f",
            format_id,
            "-o",
            str(output_path),
            self._build_video_url(video_id),
        ]
        self._run_command(command)
        if not output_path.exists():
            raise ValueError("Download completed but no output file was found.")
        return output_path

    def _extract_info(self, video_id: str) -> dict[str, Any]:
        """Extract metadata from a video without downloading."""
        command: list[str] = [
            self.executable_path,
            "--no-playlist",
            "--no-warnings",
            "-J",
            self._build_video_url(video_id),
        ]
        output: str = self._run_command(command)
        return json.loads(output)

    def _build_video_url(self, video_id: str) -> str:
        """Build a YouTube watch URL for a video."""
        return f"https://www.youtube.com/watch?v={video_id}"

    def _run_command(self, command: list[str]) -> str:
        """Run a yt-dlp command and return stdout."""
        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
