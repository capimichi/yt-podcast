FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir yt-dlp

COPY . /app

RUN mkdir -p /app/var/downloads /app/var/cache

EXPOSE 8000

CMD ["python", "-m", "ytpodcast.api"]
