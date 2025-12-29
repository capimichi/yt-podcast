"""Module for ytpodcast.mapper.controller.rss_feed_response_mapper."""

from datetime import datetime
from datetime import timezone
from email.utils import format_datetime
from xml.etree import ElementTree

from injector import inject

from ytpodcast.config.app_config import AppConfig
from ytpodcast.model.service.channel_feed import ChannelFeed
from ytpodcast.model.service.feed_item import FeedItem


# pylint: disable=too-few-public-methods
class RssFeedResponseMapper:
    """Build RSS XML responses from channel feeds."""

    @inject  # type: ignore[reportUntypedFunctionDecorator]
    def __init__(self, app_config: AppConfig) -> None:
        """Store configuration for RSS rendering."""
        self.app_config = app_config

    def create_from_feed(self, feed: ChannelFeed) -> str:
        """Serialize a channel feed into RSS XML."""
        rss_element: ElementTree.Element = ElementTree.Element("rss", version="2.0")
        channel_element: ElementTree.Element = ElementTree.SubElement(rss_element, "channel")

        ElementTree.SubElement(channel_element, "title").text = feed.get_title()
        ElementTree.SubElement(channel_element, "link").text = feed.get_url()
        ElementTree.SubElement(channel_element, "description").text = feed.get_description()
        ElementTree.SubElement(channel_element, "author").text = feed.get_author()

        image_url: str = feed.get_image_url()
        if image_url:
            image_element: ElementTree.Element = ElementTree.SubElement(channel_element, "image")
            ElementTree.SubElement(image_element, "url").text = image_url
            ElementTree.SubElement(image_element, "title").text = feed.get_title()
            ElementTree.SubElement(image_element, "link").text = feed.get_url()

        feed_items: list[FeedItem] = feed.get_items()
        if feed_items:
            latest_item: FeedItem = max(
                feed_items,
                key=lambda item: item.get_published_at(),
            )
            ElementTree.SubElement(channel_element, "lastBuildDate").text = self._format_datetime(
                latest_item.get_published_at()
            )

        for item in feed_items:
            item_element: ElementTree.Element = ElementTree.SubElement(channel_element, "item")
            ElementTree.SubElement(item_element, "title").text = item.get_title()
            ElementTree.SubElement(item_element, "link").text = item.get_url()
            ElementTree.SubElement(item_element, "description").text = item.get_description()
            guid_element: ElementTree.Element = ElementTree.SubElement(
                item_element,
                "guid",
                isPermaLink="true",
            )
            guid_element.text = item.get_url()
            ElementTree.SubElement(item_element, "pubDate").text = self._format_datetime(
                item.get_published_at()
            )
            ElementTree.SubElement(
                item_element,
                "enclosure",
                url=self._build_media_url(item),
                type="audio/mpeg",
            )

        xml_body: str = ElementTree.tostring(rss_element, encoding="unicode")
        return xml_body

    def _format_datetime(self, value: datetime) -> str:
        """Return RFC 2822 formatted datetimes for RSS feeds."""
        normalized_value: datetime = (
            value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        )
        normalized_value = normalized_value.astimezone(timezone.utc)
        return format_datetime(normalized_value)

    def _build_media_url(self, item: FeedItem) -> str:
        """Build the download URL for the feed item media."""
        base_url: str = self.app_config.api_base_url.rstrip("/")
        return f"{base_url}/videos/{item.get_video_id()}/download"
