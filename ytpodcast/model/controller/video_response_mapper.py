from ytpodcast.model.controller.video_model import VideoResponseModel
from ytpodcast.model.service.video_model import VideoModel


class VideoResponseMapper:
    """Build VideoResponseModel instances from service models."""

    def create_from_video(self, payload: VideoModel) -> VideoResponseModel:
        return VideoResponseModel(**payload.dict())
