from ytpodcast.model.controller.video_model import VideoResponseModel
from ytpodcast.model.service.video_model import VideoModel


class ServiceVideoModelToControllerVideoModelMapper:
    """Map service video model into controller video model."""

    def to_model(self, payload: VideoModel) -> VideoResponseModel:
        return VideoResponseModel(**payload.dict())
