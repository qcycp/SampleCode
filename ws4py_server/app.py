from ws4py.server.geventserver import WSGIServer
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from ws4py.websocket import WebSocket

clients = []

class WebsocketHandler(WebSocket):
    def opened(self):
        print("New client connected");
        clients.append(self)

    def received_message(self, message):
        if len(message) > 200:
            message = message[:200]+'..'
        print("receive message from client: " + str(message))
        self.send(str(message) + " was received")

    def closed(self, code, reason):
        print("client disconnected");
        clients.remove(self)

PORT=9001
server = WSGIServer(('0.0.0.0', PORT), WebSocketWSGIApplication(handler_cls=WebsocketHandler))
server.serve_forever()
