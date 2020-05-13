#blink LED -> first attempt to use Pi's pins

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) #supress warnings
GPIO.setmode(GPIO.BOARD) # referring to the pins by the numbers printed on the board (vs BCM numbers)
GPIO.setup(3, GPIO.OUT) #set as output

GPIO.output(3,0) #default to low (off)

while True:
    GPIO.output(3,1)
    time.sleep(1)
    #print("Blink: On")

    GPIO.output(3,0)
    time.sleep(1)
    #print("Blink: Off")

