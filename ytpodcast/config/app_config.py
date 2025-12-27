"""Module for ytpodcast.config.app_config."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration values."""

    app_name: str
    debug: bool
    api_host: str
    api_port: int
    api_base_url: str
    yt_api_base_url: str
    yt_api_key: str | None
    ytdl_default_format: str
