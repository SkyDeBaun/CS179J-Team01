import os
import sys
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import RPi.GPIO as GPIO
from decimal import Decimal
import json

# Callback function that is triggered when the topic subscribed to gets new published data
fanOn = False
print("Fan is off.")
print("####")
def myCallBack(self, params, packet):
    global fanOn
    payloadDict = json.loads(packet.payload)
    humidity = Decimal(payloadDict["humidity"])
    #print(humidity)
    if (humidity > 85 and fanOn is False):
        print("Fan turning on...")
        print("####")
        GPIO.output(16, GPIO.LOW)
        fanOn = True

    elif (humidity <= 85 and fanOn is True):
        print("Fan turning off...")
        print("####")
        GPIO.output(16, GPIO.HIGH)
        fanOn = False


# Setup pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Specifiy the pin that will control the DC fan
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)

myMQTTClient = AWSIoTMQTTClient("myClientIDSub")
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA.crt","/home/pi/AWS_certs/1aac3835be-private.pem.key","/home/pi/AWS_certs/1aac3835be-certificate.pem.crt")


# AWSIoTMQTTClient connection configuration
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.subscribe("ryan_pi/data", 1, myCallBack)

while True:
    continue
