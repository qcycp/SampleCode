import threading
import time
import websocket
from urllib.parse import urlencode

port = 9001

def on_message(ws, message):
    print("receive message from server: " + message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def job():
        while True:
            time.sleep(5)
            ws.send("Hello")
        time.sleep(1)
        ws.close()
    thread = threading.Thread(target=job)
    thread.start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    url = {'params': 'test'}
    ws = websocket.WebSocketApp("ws://127.0.0.1:" + str(port) + "/ws?" + urlencode(url),
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
