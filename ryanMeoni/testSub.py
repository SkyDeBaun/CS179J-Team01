import os
import sys
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

# Callback function that is triggered when the topic subscribed to gets new published data
def myCallBack(self, params, packet):
        print(packet.payload)


myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA_1.pem","/home/pi/AWS_certs/1aac3835be-private.pem.key","/home/pi/AWS_certs/1aac3835be-certificate.pem.crt")


# AWSIoTMQTTClient connection configuration
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.subscribe("ryanpi/data", 1, myCallBack)

while True:
        continue
