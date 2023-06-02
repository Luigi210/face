from pyfirmata import Arduino, SERVO, OUTPUT, PWM
import pyfirmata
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
from PyMata.pymata import PyMata
import time
# import board
# import pulseio
for port in ports:
    print(port.device)

board = Arduino('/dev/cu.usbmodem1101')

servo_13_pin = 13
servo_13 = board.get_pin('d:{}:s'.format(servo_13_pin))
led_8_pin = 8
led_9_pin = 9
buzzer_pin = 12
buzzer = board.get_pin('d:{}:s'.format(buzzer_pin))
print(servo_13, buzzer, board)

board.digital[led_8_pin].mode = OUTPUT
board.digital[led_9_pin].mode = OUTPUT
board.digital[buzzer_pin].mode = OUTPUT
board.digital[servo_13_pin].mode = SERVO


while True:
    print("Running")
    board.digital[servo_13_pin].write(90)
    board.digital[led_8_pin].write(0)
    board.digital[led_9_pin].write(0)
    board.play_tone(buzzer_pin, board.TONE_TONE, 1000, 10)
    board.digital[buzzer_pin].write(1)  # Turn the buzzer on
    #board.send_sysex(pyfirmata.TONE_DATA, (int(567), 1000)) 
    #board.play_tone(buzzer_pin, board.TONE_TONE, 1000, 10)
    board.send_sysex('0x40 0x20 0x38 0x03 0x50 0x0F') 
    board.pass_time(2)
    board.digital[servo_13_pin].write(180)
    board.digital[led_8_pin].write(1)
    board.digital[led_9_pin].write(1)
    # board.digital[buzzer_pin].write(0) 


  
    #board.set_pin_mode(buzzer_pin, pyfirmata.TONE)  # Set the pin to generate a tone
   
    #board.send_sysex(pyfirmata.TONE_DATA, (int(567), 1000))  # Set the tone frequency and duration
    #time.sleep(2)  # Play the tone for 1 second
    #board.set_pin_mode(buzzer_pin, pyfirmata.TONE)  # Set the pin to generate a tone
    #board.send_sysex(pyfirmata.TONE_DATA, (int(120), 1000))  # Set the tone frequency and duration
    