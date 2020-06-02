#Photovoltaic IR sensor -> turn on LED when warm body detected, else turn off

import RPi.GPIO as GPIO
import time
from os import system, name 
from time import sleep 

#clear screen function----------------------
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


#GPIO config-------------------------------
GPIO.setwarnings(False) #supress warnings
GPIO.setmode(GPIO.BOARD) # referring to the pins by the numbers printed on the board (vs BCM numbers)
GPIO.setup(3, GPIO.OUT) #set as output -> LED
GPIO.setup(7, GPIO.IN) #input pin for PIR sensor
GPIO.output(3,0) #LED default to low (off)



#loop for signal/control------------------
while True:
    signal = GPIO.input(7)
    print(signal)

    if signal == 0:
        #nobody detected -----------------
        GPIO.output(3,0) #LED off
        print("Nobody detected")
        sleep(1)


    elif signal == 1:
        #body detected --------------------
        GPIO.output(3,1) #LED on
        print("Somebody detected")
        sleep(1)

    clear()

    


