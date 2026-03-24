FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir yt-dlp

COPY . /app

RUN chmod +x /app/docker/entrypoint.sh /app/docker/update-yt-dlp.sh \
    && chmod 0644 /app/docker/yt-dlp.cron /app/docker/pending-downloads.cron \
    && cp /app/docker/yt-dlp.cron /etc/cron.d/yt-dlp-update \
    && cp /app/docker/pending-downloads.cron /etc/cron.d/pending-downloads

RUN mkdir -p /app/var/downloads /app/var/cache /app/var/log

EXPOSE 8000

CMD ["/app/docker/entrypoint.sh"]
