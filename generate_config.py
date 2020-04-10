import sys

SOURCE_URLS = sys.argv[1]
STREAM_NAMES = sys.argv[2]
RTSP_PROXY_SOURCE_TCP = sys.argv[3]

yaml = \
"server:\n" +
"  # supported protocols\n" +
"  protocols: [ tcp, udp ]\n" +
"  # port of the RTSP UDP/TCP listener\n" +
"  rtspPort: 8554\n" +
"  # port of the RTP UDP listener\n" +
"  rtpPort: 8000\n" +
"  # port of the RTCP UDP listener\n" +
"  rtcpPort: 8001\n" +

"streams:\n"

stream_urls = ",".split(SOURCE_URLS)
stream_names = ",".split(STREAM_NAMES)

if len(stream_urls) != len(stream_names):
  raise ValueError('Number of STREAM_NAMES must match number of SOURCE_URLS')
  
for i in range(stream_urls):
  url = stream_urls[i]
  name = stream_names[i]
  
  yaml += \
  name + ":\n" +
  "  url: " + url + "\n" +
  "  # whether to receive this stream in udp or tcp\n" +
  "  useTcp: " + RTSP_PROXY_SOURCE_TCP + "\n"

print(yaml)
