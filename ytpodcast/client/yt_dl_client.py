"""Module for ytpodcast.client.yt_dl_client."""

import json
import subprocess
import tempfile
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
        ytdl_executable_path: str,
        ffmpeg_executable_path: str,
    ) -> None:
        """Store default audio format settings."""
        self.default_format = default_format
        self.download_dir = download_dir
        self.ytdl_executable_path = ytdl_executable_path
        self.ffmpeg_executable_path = ffmpeg_executable_path

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

    def download_audio(self, video_id: str, format_id: str) -> Path:
        """Download a single audio format for a video."""
        download_dir_path: Path = Path(self.download_dir)
        download_dir_path.mkdir(parents=True, exist_ok=True)
        output_path: Path = download_dir_path / f"{video_id}.mp3"
        if output_path.exists():
            return output_path
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path: Path = Path(temp_dir)
            temp_output_path: Path = temp_dir_path / f"{video_id}.%(ext)s"
            command: list[str] = [
                self.ytdl_executable_path,
                "--no-playlist",
                "--quiet",
                "--no-warnings",
                "-f",
                format_id,
                "-o",
                str(temp_output_path),
                self._build_video_url(video_id),
            ]
            self._run_command(command)
            downloaded_files: list[Path] = [
                path for path in temp_dir_path.iterdir() if path.is_file()
            ]
            if not downloaded_files:
                raise ValueError("Download completed but no output file was found.")
            source_path: Path = downloaded_files[0]
            self._convert_to_mp3(source_path, output_path)
        if not output_path.exists():
            raise ValueError("MP3 conversion completed but no output file was found.")
        return output_path

    def _extract_info(self, video_id: str) -> dict[str, Any]:
        """Extract metadata from a video without downloading."""
        command: list[str] = [
            self.ytdl_executable_path,
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

    def _convert_to_mp3(self, source_path: Path, output_path: Path) -> None:
        """Convert a downloaded audio file to MP3."""
        command: list[str] = [
            self.ffmpeg_executable_path,
            "-y",
            "-i",
            str(source_path),
            str(output_path),
        ]
        self._run_command(command)
