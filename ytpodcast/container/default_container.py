"""Module for ytpodcast.container.default_container."""

import os
from typing import Any, TypeVar

from dotenv import load_dotenv
from injector import Injector

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.client.yt_dl_client import YtDlClient
from ytpodcast.config.app_config import AppConfig
from ytpodcast.controller.channel_controller import ChannelController
from ytpodcast.controller.video_controller import VideoController
from ytpodcast.controller.feed_controller import FeedController
from ytpodcast.mapper.controller.get_channel_response_mapper import GetChannelResponseMapper
from ytpodcast.mapper.controller.get_video_response_mapper import GetVideoResponseMapper
from ytpodcast.mapper.controller.rss_feed_response_mapper import RssFeedResponseMapper
from ytpodcast.mapper.controller.file_response_mapper import FileResponseMapper
from ytpodcast.mapper.service.channel_mapper import ChannelMapper
from ytpodcast.mapper.service.video_mapper import VideoMapper
from ytpodcast.mapper.service.feed_item_mapper import FeedItemMapper
from ytpodcast.service.channel_service import ChannelService
from ytpodcast.service.video_service import VideoService
from ytpodcast.helper.file_helper import FileHelper
from ytpodcast.service.feed_service import FeedService


# pylint: disable=too-many-instance-attributes
T = TypeVar("T")


class DefaultContainer:
    """Dependency container for the ytpodcast service."""

    injector = None
    instance = None

    @staticmethod
    def get_instance():
        """Return the shared container instance."""
        if DefaultContainer.instance is None:
            DefaultContainer.instance = DefaultContainer()
        return DefaultContainer.instance

    def __init__(self) -> None:
        """Initialize dependency bindings and environment."""
        self.injector = Injector()
        load_dotenv()
        self._init_environment_variables()
        self._init_bindings()

    def get(self, key: type[T]) -> T:
        """Resolve a dependency by key from the injector."""
        return self.injector.get(key)

    def get_var(self, key: str) -> Any:
        """Return a stored environment variable by key."""
        return self.__dict__[key]

    def _init_environment_variables(self) -> None:
        """Load environment variables into container fields."""
        self.app_name = os.environ.get("APP_NAME", "YT Podcast API")
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.api_host = os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = int(os.environ.get("API_PORT", "8459"))
        self.api_base_url = os.environ.get(
            "API_BASE_URL",
            f"http://localhost:{self.api_port}",
        )
        self.yt_api_base_url = os.environ.get("YT_API_BASE_URL", "https://youtube.googleapis.com")
        self.yt_api_key = os.environ.get("YT_API_KEY")
        self.ytdl_default_format = os.environ.get("YTDL_DEFAULT_FORMAT", "bestaudio")
        self.download_dir = os.environ.get("DOWNLOAD_DIR", os.path.join("var", "downloads"))
        self.ytdl_executable_path = os.environ.get("YTDL_EXECUTABLE_PATH", "yt-dlp")
        self.ffmpeg_executable_path = os.environ.get("FFMPEG_EXECUTABLE_PATH", "ffmpeg")

    def _init_bindings(self) -> None:
        """Bind configured services, mappers, and clients."""
        app_config = AppConfig(
            app_name=self.app_name,
            debug=self.debug,
            api_host=self.api_host,
            api_port=self.api_port,
            api_base_url=self.api_base_url,
            yt_api_base_url=self.yt_api_base_url,
            yt_api_key=self.yt_api_key,
            ytdl_default_format=self.ytdl_default_format,
        )
        self.injector.binder.bind(AppConfig, to=app_config)

        channel_mapper = ChannelMapper()
        self.injector.binder.bind(ChannelMapper, to=channel_mapper)

        video_mapper = VideoMapper()
        self.injector.binder.bind(VideoMapper, to=video_mapper)

        file_helper = FileHelper()
        self.injector.binder.bind(FileHelper, to=file_helper)

        channel_response_mapper = GetChannelResponseMapper()
        self.injector.binder.bind(GetChannelResponseMapper, to=channel_response_mapper)

        video_response_mapper = GetVideoResponseMapper()
        self.injector.binder.bind(GetVideoResponseMapper, to=video_response_mapper)

        file_response_mapper = FileResponseMapper(file_helper)
        self.injector.binder.bind(FileResponseMapper, to=file_response_mapper)

        feed_item_mapper = FeedItemMapper()
        self.injector.binder.bind(FeedItemMapper, to=feed_item_mapper)

        rss_feed_response_mapper = RssFeedResponseMapper(app_config)
        self.injector.binder.bind(RssFeedResponseMapper, to=rss_feed_response_mapper)

        yt_api_client = YtApiClient(
            base_url=self.yt_api_base_url,
            api_key=self.yt_api_key,
        )
        self.injector.binder.bind(YtApiClient, to=yt_api_client)

        yt_dl_client = YtDlClient(
            default_format=self.ytdl_default_format,
            download_dir=self.download_dir,
            ytdl_executable_path=self.ytdl_executable_path,
            ffmpeg_executable_path=self.ffmpeg_executable_path,
        )
        self.injector.binder.bind(YtDlClient, to=yt_dl_client)

        channel_service = ChannelService(yt_api_client, channel_mapper)
        self.injector.binder.bind(ChannelService, to=channel_service)

        video_service = VideoService(
            yt_api_client,
            yt_dl_client,
            video_mapper,
        )
        self.injector.binder.bind(VideoService, to=video_service)

        feed_service = FeedService(yt_api_client, channel_mapper, feed_item_mapper)
        self.injector.binder.bind(FeedService, to=feed_service)

        channel_controller = ChannelController(
            channel_service,
            channel_response_mapper,
        )
        self.injector.binder.bind(ChannelController, to=channel_controller)

        video_controller = VideoController(
            video_service,
            video_response_mapper,
            file_response_mapper,
        )
        self.injector.binder.bind(VideoController, to=video_controller)

        feed_controller = FeedController(feed_service, rss_feed_response_mapper)
        self.injector.binder.bind(FeedController, to=feed_controller)
