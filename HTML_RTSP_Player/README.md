#### Pre-requires
* download ffmpeg for windows
https://www.ffmpeg.org/download.html#build-windows
* install nodejs

#### websocket and http server
```
$ cd server
$ npm install ws
$ node websocket.js secret 8081 8082
```
* "secret" is a code to indicate 
* http server port is 8081
* websocket port is 8082

#### ffmpeg player
```
$ cd ffmpeg/bin
$ ffmpeg -rtsp_transport tcp -i rtsp://10.60.6.28:8554/CH001.sdp -r 20 -q 0 -f mpegts -codec:v mpeg1video -codec:a mp2 -s 1280x720 http://127.0.0.1:8081/supersecret/live1
-rtsp_transport tcp: receive rtsp streaming input via tcp
-i rtsp://10.60.6.28:8554/CH001.sdp: rtsp streaming input
-r 20: set output frame rate, MPEG-1/2 does not support 15/1 fps
-q 0: use fixed quality scale
-f mpegts: set force output format
-codec:v mpeg1video: set output video codec
-codec:a mp2:  set output audio codec
-s 1280x720: set output frame size
```

#### Webpage
```
$ cd client
$ open index.html
```