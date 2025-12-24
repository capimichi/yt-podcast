from pydantic import BaseModel


class YtApiChannelModel(BaseModel):
    """Channel payload from the YouTube API."""

    channel_id: str
    title: str
    description: str
    url: str
