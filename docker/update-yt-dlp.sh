#!/bin/sh
set -eu

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

printf '[%s] Starting yt-dlp update\n' "$(timestamp)"
/usr/local/bin/python -m pip install --no-cache-dir --upgrade yt-dlp
printf '[%s] Completed yt-dlp update\n' "$(timestamp)"
