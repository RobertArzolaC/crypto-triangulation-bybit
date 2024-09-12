from dotenv import load_dotenv

from exchange_websocket import ExchangeWebSocket
from constants import FIRST_PAIR, SECOND_PAIR, THIRD_PAIR, PAIRS_CRIPTO
from observers import PriceBinanceObserver


load_dotenv()


def main():
    exchange_websocket = ExchangeWebSocket(PAIRS_CRIPTO)

    first_pair_observer = PriceBinanceObserver(FIRST_PAIR)
    second_pair_observer = PriceBinanceObserver(SECOND_PAIR)
    third_pair_observer = PriceBinanceObserver(THIRD_PAIR)

    exchange_websocket.register_observer(first_pair_observer)
    exchange_websocket.register_observer(second_pair_observer)
    exchange_websocket.register_observer(third_pair_observer)

    exchange_websocket.start()


if __name__ == "__main__":
    main()
