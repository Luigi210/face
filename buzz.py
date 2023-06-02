import time
import sys
import signal

from PyMata.pymata import PyMata


BEEPER = 12  # pin that piezo device is attached to

# create a PyMata instance
board = PyMata("/dev/cu.usbmodem1101")


def signal_handler(sig, frm):
    print('You pressed Ctrl+C!!!!')
    if board is not None:
        board.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

for i in range(10):
    board.play_tone(BEEPER, board.TONE_TONE, 1000, 10)
    time.sleep(1)

board.close()