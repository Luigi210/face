import sys
import time
from pymata4 import pymata4

"""
This is a demonstration of the tone methods
"""

# instantiate pymata4
board = pymata4.Pymata4("/dev/cu.usbmodem14101")
TONE_PIN=12
try:
    # set a pin's mode for tone operations
    board.set_pin_mode_tone(TONE_PIN)

    # specify pin, frequency and duration and play tone
    board.play_tone(TONE_PIN, 1000, 500)
    time.sleep(2)

    # specify pin and frequency and play continuously
    board.play_tone_continuously(TONE_PIN, 2000)
    time.sleep(2)

    # specify pin to turn pin off
    board.play_tone_off(TONE_PIN)

    # clean up
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)