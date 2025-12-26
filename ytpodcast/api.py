"""Module for ytpodcast.api."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import RedirectResponse

from ytpodcast.config.app_config import AppConfig
from ytpodcast.container.default_container import DefaultContainer
from ytpodcast.controller.channel_controller import ChannelController
from ytpodcast.controller.feed_controller import FeedController
from ytpodcast.controller.video_controller import VideoController


default_container: DefaultContainer = DefaultContainer.get_instance()
app_config: AppConfig = default_container.get(AppConfig)

app = FastAPI(
    title=app_config.app_name,
    description="YT podcast API",
    version="1.0.0",
)

channel_controller: ChannelController = default_container.get(ChannelController)
feed_controller: FeedController = default_container.get(FeedController)
video_controller: VideoController = default_container.get(VideoController)

app.include_router(channel_controller.router)
app.include_router(feed_controller.router)
app.include_router(video_controller.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to the API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
async def health_check():
    """Return a basic health payload."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "ytpodcast.api:app",
        host=app_config.api_host,
        port=app_config.api_port,
        reload=False,
    )
