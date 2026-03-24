#!/bin/sh
set -eu

mkdir -p /app/var/downloads /app/var/cache /app/var/log
touch /app/var/log/yt-dlp-update.log
touch /app/var/log/pending-downloads.log

cron

exec python -m ytpodcast.api
