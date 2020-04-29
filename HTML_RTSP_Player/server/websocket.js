var fs = require('fs');
var http = require('http');
var WebSocket = require('ws');

if (process.argv.length < 3) {
	console.log('Invalid parameter!');
	process.exit();
}

var stream_secret = process.argv[2];//secret code
var stream_port = process.argv[3] || 8081;//ffmpeg port
var websocket_port = process.argv[4] || 8082;//websocket port
var record_stream = false;
var totalSize = 0;

function initWebSocket(websocket_port) {
	var clientMap = new Map();//buffer to implement multiple rtsp streaming playing at the same time
	var socketServer = new WebSocket.Server({
		port : websocket_port,
		perMessageDeflate : false
	});
	socketServer.on('connection', function(socket, upgradeReq) {
		var url = upgradeReq.socket.remoteAddress + upgradeReq.url;
		var key = url.substr(1).split('/')[1];//key value to indicate rtsp streaming
		var clients = clientMap.get(key);
		if(!clients){
			clients = new Set();
			clientMap.set(key,clients);
		}
		clients.add(socket);
		totalSize++;
		console.log("A new connection, the current number of connections: " + totalSize);
		socket.on('close', function(code, message) {
			var clientSet = clientMap.get(key);
			if(clientSet){
				clientSet.delete(socket);
				totalSize--;
				if(clientSet.size == 0){
					clientMap.delete(key);
				}
			}
			console.log("A connection closed, the current number of connections: " + totalSize);
		});
	});

	socketServer.broadcast = function(data, theme) {
		var clients = clientMap.get(theme);
		if (clients) {
			clients.forEach(function (client, set) {
				if(client.readyState === WebSocket.OPEN){
					client.send(data);
				}
			});
		}
	};
	return socketServer;
}

function initHttp(stream_port, stream_secret, record_stream, socketServer) {
	var streamServer = http.createServer(
			function(request, response) {
				var params = request.url.substr(1).split('/');
				if (params.length != 2) {
					console.log("Invalid parameter!");
					response.end();
				}
				if (params[0] !== stream_secret) {
					console.log("Secret code is incorrect: " + request.socket.remoteAddress + ":" + request.socket.remotePort);
					response.end();
				}
				response.connection.setTimeout(0);
				request.on('data', function(data) {
					socketServer.broadcast(data, params[1]);
					if (request.socket.recording) {
						request.socket.recording.write(data);
					}
				});
				request.on('end', function() {
					console.log("Request closed");
					if (request.socket.recording) {
						request.socket.recording.close();
					}
				});
				if (record_stream) {
					var path = 'recordings/' + Date.now() + '.ts';
					request.socket.recording = fs.createWriteStream(path);
				}
			}).listen(stream_port);
			console.log('Server is starting...');
}

initHttp(stream_port, stream_secret, record_stream, initWebSocket(websocket_port));