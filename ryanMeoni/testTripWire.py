import RPi.GPIO as GPIO                   #Import GPIO library
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep

# Wait 1 second at startup (necessary for tripwire)
sleep(1)

# Only want to publish once to cloud for testing, use a boolean
alreadyRan = False
# Event that will trigger once pin 21 is no longer high (the laser has been blocked by something)
def event(ev=None):
        global alreadyRan
        if alreadyRan is False:
                payload = '{"Temperature": ' + "yessir!" +'}'
                print(payload)
                myMQTTClient.connect()
                myMQTTClient.publish("ryanpi/data", payload, 0)
                alreadyRan = True

# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(21, GPIO.FALLING, callback=event)

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint("ayvv068gcr0us-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA_1.pem", "/home/pi/AWS_certs/baab1eaf4e-private.pem.key", "/home/pi/AWS_certs/baab1eaf4e-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

while 1:
        continue
