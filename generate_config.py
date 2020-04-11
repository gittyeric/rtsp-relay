import sys

SOURCE_URLS = sys.argv[1]
STREAM_NAMES = sys.argv[2]
RTSP_PROXY_SOURCE_TCP = sys.argv[3]

stream_urls = SOURCE_URLS.split(",")
stream_names = STREAM_NAMES.split(",")
stream_count = len(stream_urls)

if STREAM_NAMES == "" or len(stream_names) == 0:
  stream_names = "stream"
  if stream_count == 1:
    stream_names = ["stream" + ((i+1) for i in range(len(stream_urls)))]

if stream_count != len(stream_names):
  raise ValueError('Number of STREAM_NAMES must match number of SOURCE_URLS')

yaml = \
"server:\n" + \
"  # supported protocols\n" + \
"  protocols: [ tcp, udp ]\n" + \
"  # port of the RTSP UDP/TCP listener\n" + \
"  rtspPort: 8554\n" + \
"  # port of the RTP UDP listener\n" + \
"  rtpPort: 8000\n" + \
"  # port of the RTCP UDP listener\n" + \
"  rtcpPort: 8001\n" + \
"streams:\n"

start_script = "#!bash\n\n"

for i in range(len(stream_urls)):
  url = stream_urls[i]
  name = stream_names[i]

  yaml += \
  name + ":\n" + \
  "  url: " + url + "\n" + \
  "  # whether to receive this stream in udp or tcp\n" + \
  "  useTcp: " + RTSP_PROXY_SOURCE_TCP + "\n"

  start_script += "sh start-proxy-" + str(i) + ".sh &;\n"

  # Generate start-proxy-x.sh
  sh = \
  '#!/bin/bash' + \
  'echo "Start relaying from ' + url + ' to rtsp://0.0.0.0:8554/' + name + '"\n' + \
  'while true; do\n' + \
  'set -x\n' + \
  'ffmpeg $FFMPEG_INPUT_ARGS -i ' + url + ' $FFMPEG_OUTPUT_ARGS -f rtsp rtsp://127.0.0.1:8554/' + name + '\n' + \
  'set +x\n' + \
  'echo "Reconnecting..."\n' + \
  'sleep 1\n' + \
  'done'

  with open("start-proxy-" + str(i), "w") as proxy_runner:
    proxy_runner.write(sh)

with open("start-all.sh", "w") as start_all:
  start_all.write(start_script)

with open("proxy.yaml", "w") as config:
  config.write(yaml)
