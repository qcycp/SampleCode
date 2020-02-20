import time
from websocket_server import WebsocketServer

clients = []

def new_client(client, server):
    clients.append(client)
    print(clients)
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("New client connected and was given id %d" % client['id'])

def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])
    clients.remove(client)

def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message(client, message + " was received")

PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
