import RPi.GPIO as GPIO                   #Import GPIO library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import functionalizedAWSIOT

# Wait 1 second at startup (necessary for tripwire)
sleep(1)

# Only want to publish once to cloud for testing, use a boolean
# Event that will trigger once pin 21 is no longer high (the laser has been blocked by something)
def event(ev=None):
        payload = 'Triggered'
        print("Triggered")
        myMQTTClient.publish("ryan_pi/data", payload, 0)


# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.add_event_detect(21, GPIO.FALLING, callback = event, bouncetime = 5000)

# AWS IoT certificate based connection
myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
while 1:
        continue

