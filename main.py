import signal
import sys

from app.helpers import csv_maker
from app.modules.telegram import Telegram

telegram = None


def main():
    global telegram

    if len(sys.argv) < 1:
        return print('Please specify a query')

    depth = sys.argv[2] if len(sys.argv) >= 2 else 0

    telegram = Telegram(
        sys.argv[1],
        depth=int(depth)
    )


main()


def signal_handler(sig, frame):
    if telegram:
        csv_maker.make_csv_file(list(telegram.results.values()))

    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
signal.pause()
