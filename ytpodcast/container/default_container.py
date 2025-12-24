import os

from dotenv import load_dotenv
from injector import Injector

from ytpodcast.client.yt_api_client import YtApiClient
from ytpodcast.client.yt_dl_client import YtDlClient
from ytpodcast.config.app_config import AppConfig
from ytpodcast.controller.channel_controller import ChannelController
from ytpodcast.controller.video_controller import VideoController
from ytpodcast.model.controller.channel_response_mapper import ChannelResponseMapper
from ytpodcast.model.controller.video_response_mapper import VideoResponseMapper
from ytpodcast.model.controller.xml_response_mapper import XmlResponseMapper
from ytpodcast.model.service.channel_mapper import ChannelMapper
from ytpodcast.model.service.video_mapper import VideoMapper
from ytpodcast.service.channel_service import ChannelService
from ytpodcast.service.video_service import VideoService


class DefaultContainer:
    """Dependency container for the ytpodcast service."""

    injector = None
    instance = None

    @staticmethod
    def getInstance():
        if DefaultContainer.instance is None:
            DefaultContainer.instance = DefaultContainer()
        return DefaultContainer.instance

    def __init__(self) -> None:
        self.injector = Injector()
        load_dotenv()
        self._init_environment_variables()
        self._init_bindings()

    def get(self, key):
        return self.injector.get(key)

    def get_var(self, key):
        return self.__dict__[key]

    def _init_environment_variables(self) -> None:
        self.app_name = os.environ.get("APP_NAME", "YT Podcast API")
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.api_host = os.environ.get("API_HOST", "0.0.0.0")
        self.api_port = int(os.environ.get("API_PORT", "8459"))
        self.yt_api_base_url = os.environ.get("YT_API_BASE_URL", "https://youtube.googleapis.com")
        self.yt_api_key = os.environ.get("YT_API_KEY")
        self.ytdl_default_format = os.environ.get("YTDL_DEFAULT_FORMAT", "bestaudio")

    def _init_bindings(self) -> None:
        app_config = AppConfig(
            app_name=self.app_name,
            debug=self.debug,
            api_host=self.api_host,
            api_port=self.api_port,
            yt_api_base_url=self.yt_api_base_url,
            yt_api_key=self.yt_api_key,
            ytdl_default_format=self.ytdl_default_format,
        )
        self.injector.binder.bind(AppConfig, to=app_config)

        channel_mapper = ChannelMapper()
        self.injector.binder.bind(ChannelMapper, to=channel_mapper)

        video_mapper = VideoMapper()
        self.injector.binder.bind(VideoMapper, to=video_mapper)

        channel_response_mapper = ChannelResponseMapper()
        self.injector.binder.bind(ChannelResponseMapper, to=channel_response_mapper)

        video_response_mapper = VideoResponseMapper()
        self.injector.binder.bind(VideoResponseMapper, to=video_response_mapper)

        xml_response_mapper = XmlResponseMapper()
        self.injector.binder.bind(XmlResponseMapper, to=xml_response_mapper)

        yt_api_client = YtApiClient(
            base_url=self.yt_api_base_url,
            api_key=self.yt_api_key,
        )
        self.injector.binder.bind(YtApiClient, to=yt_api_client)

        yt_dl_client = YtDlClient(default_format=self.ytdl_default_format)
        self.injector.binder.bind(YtDlClient, to=yt_dl_client)

        channel_service = ChannelService(yt_api_client, channel_mapper)
        self.injector.binder.bind(ChannelService, to=channel_service)

        video_service = VideoService(yt_api_client, yt_dl_client, video_mapper)
        self.injector.binder.bind(VideoService, to=video_service)

        channel_controller = ChannelController(
            channel_service,
            channel_response_mapper,
            xml_response_mapper,
        )
        self.injector.binder.bind(ChannelController, to=channel_controller)

        video_controller = VideoController(
            video_service,
            video_response_mapper,
            xml_response_mapper,
        )
        self.injector.binder.bind(VideoController, to=video_controller)
