from pydantic import BaseModel


class ChannelResponseModel(BaseModel):
    """Response payload for channel routes."""

    channel_id: str
    title: str
    description: str
    url: str
