#!/bin/bash

while true; do
  set -x
  ffmpeg $FFMPEG_INPUT_ARGS -i $SOURCE_URLS $FFMPEG_OUTPUT_ARGS -f rtsp rtsp://127.0.0.1:8554/$STREAM_NAME
  set +x
  echo "Reconnecting..."
  sleep 1
done
