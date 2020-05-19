import RPi.GPIO as GPIO  # Import GPIO library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import functionalizedAWSIOT

# Wait 1 second at startup (necessary for tripwire)
sleep(1)

# Only want to publish once to cloud for testing, use a boolean
# Event that will trigger once pin 21 is no longer high (the laser has been blocked by something)


def event(ev=None):
    test = "does not matter"
    payload = test
    print("Triggered")
    myMQTTClient.publish("CameraModule/Camera1/picture", payload, 0)


# initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(21, GPIO.FALLING, callback=event, bouncetime=5000)

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint(
    "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA.crt",
                                  "/home/pi/AWS_certs/1aac3835be-private.pem.key", "/home/pi/AWS_certs/1aac3835be-certificate.pem.crt")
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()

while 1:
    continue
