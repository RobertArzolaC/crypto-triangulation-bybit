import json

import websocket

from constants import EXCHANGE_WEBSOCKET_URL, LOG_FILE_PATH
from logger import CryptoLogger


logger = CryptoLogger(__name__, file_path=LOG_FILE_PATH)


class ExchangeWebSocket:
    def __init__(self, pairs):
        self.pairs = pairs
        self.socket = None
        self.observers = []
        self.url = EXCHANGE_WEBSOCKET_URL

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

    def get_args(self):
        return [f"bookticker.{pair}" for pair in self.pairs]

    def start(self):
        websocket.enableTrace(True)
        self.socket = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_error=self.on_error,
            on_message=self.on_message,
        )
        logger.info("Starting handle for websocket ...")
        self.socket.run_forever(reconnect=15)

    def on_open(self, ws):
        subscribe_message = {
            "req_id": "10001",
            "op": "subscribe",
            "args": self.get_args(),
        }
        ws.send(json.dumps(subscribe_message))

    def on_message(self, ws, message):
        data = json.loads(message)
        self.notify_observers(data)

    def on_error(self, ws, error):
        logger.error(f"Error on websocket: {error}")
