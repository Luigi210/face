from pyfirmata import Arduino, SERVO, OUTPUT, PWM
import pyfirmata
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
import time

for port in ports:
    print(port.device)

board = Arduino('/dev/cu.usbmodem1101')

servo_13_pin = 13
servo_13 = board.get_pin('d:{}:s'.format(servo_13_pin))
led_8_pin = 8
led_9_pin = 9
servo_12_pin = 12
servo_12 = board.get_pin('d:{}:s'.format(servo_12_pin))

print(servo_13, servo_12, board)

board.digital[led_8_pin].mode = OUTPUT
board.digital[led_9_pin].mode = OUTPUT
board.digital[servo_12_pin].mode = SERVO
board.digital[servo_13_pin].mode = SERVO


while True:
    print("Running")
    board.digital[servo_13_pin].write(90)
    board.digital[servo_12_pin].write(90)
    board.digital[led_8_pin].write(0)
    board.digital[led_9_pin].write(0)
# Turn the buzzer on


    board.pass_time(2)
    board.digital[servo_13_pin].write(180)
    board.digital[servo_12_pin].write(180)
    board.digital[led_8_pin].write(1)
    board.digital[led_9_pin].write(1)
    # board.digital[buzzer_pin].write(0) 


  
    #board.set_pin_mode(buzzer_pin, pyfirmata.TONE)  # Set the pin to generate a tone

    #time.sleep(2)  # Play the tone for 1 second
    #board.set_pin_mode(buzzer_pin, pyfirmata.TONE)  # Set the pin to generate a tone    