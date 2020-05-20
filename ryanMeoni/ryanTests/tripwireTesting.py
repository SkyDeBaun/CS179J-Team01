import RPi.GPIO as GPIO                   #Import GPIO library
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep

# Wait 1 second at startup (necessary for tripwire)
sleep(1)

# Event that will trigger once pin 21 is no longer high (the laser has been blocked by something)
def event(ev=None):
        print("Tripwire activated")

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(21, GPIO.FALLING, callback=event, bouncetime = 5000)


while 1:
        continue
