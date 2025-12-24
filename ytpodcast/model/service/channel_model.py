from pydantic import BaseModel


class ChannelModel(BaseModel):
    """Domain model for a YouTube channel."""

    channel_id: str
    title: str
    description: str
    url: str
