#!/bin/sh
set -eu

mkdir -p /app/var/downloads /app/var/cache /var/log
touch /var/log/yt-dlp-update.log

cron

exec python -m ytpodcast.api
