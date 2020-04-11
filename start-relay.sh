#!/bin/bash

set -e

# Backwards compat
if [[ $SOURCE_URLS == "" ]] && [ $SOURCE_URL != "" ]; then
  export SOURCE_URLS=$SOURCE_URL
fi
if [[ $STREAM_NAMES == "" ]] && [ $STREAM_NAME != "" ]; then
  export STREAM_NAMES=$STREAM_NAME
fi

if [[ $SOURCE_URLS == file://* ]]; then
   export FFMPEG_INPUT_ARGS="$FFMPEG_INPUT_ARGS -re -stream_loop -1"
fi

touch proxy.yaml
python generate_config.py "$SOURCE_URLS" "$STREAM_NAMES" RTSP_PROXY_SOURCE_TCP

if [[ $SOURCE_URLS == rtsp://* ]] && [ "$FORCE_FFMPEG_SOURCE" == "false" ]; then
   echo "Starting rtsp proxy from $SOURCE_URLS to rtsp://0.0.0.0:8554/<$STREAM_NAMES>"
   rtsp-simple-proxy /proxy.yml
else

   if [ "$SOURCE_URLS" != "" ]; then
      echo "Starting rtsp server..."
      rtsp-simple-server &
      sleep 2

      start-proxies.sh
   else
      echo "Won't restream a source feed to the server because SOURCE_URLS was not defined"
      echo "Starting rtsp server. You can publish feeds to it (ex.: ffmpeg -i somesource.mjpg -c copy -f rtsp rtsp://localhost:8554/myfeed)"
      rtsp-simple-server
   fi
fi
