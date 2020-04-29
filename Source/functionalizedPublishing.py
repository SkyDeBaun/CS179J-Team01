from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTThingJobsClient
from time import sleep
from datetime import date, datetime

import subprocess

CLIENT = "333052c1bf"
AWS_SERVER = "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com"
PORT = 8883

CA_CERTIFICATE = "../Certificates/root-CA.crt"
PRIVATE_KEY = "../Certificates/device-private.pem.key"
DEVICE_CERTIFICATE = "../Certificates/device-certificate.pem.crt"

DEVICE_TYPE = "CameraModule"
THING_NAME = "Camera1"
TOPICS = ["picture", "stream", "video"]

def AWS_MQTT_subscribe():
    #TODO
    return

def AWS_MQTT_Initialize():
  subprocess.call('./copyCertificates.sh')
  # AWS IoT certificate based connection---------------------------------------
  myMQTTClient = AWSIoTMQTTClient(CLIENT)#this can be any arbitrary string
  myMQTTClient.configureEndpoint(AWS_SERVER, PORT)#endpoint and port number
  myMQTTClient.configureCredentials(CA_CERTIFICATE, PRIVATE_KEY, DEVICE_CERTIFICATE)#root ca and certificate used for secure connection

  myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
  myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
  myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
  myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
  #connect and publish----------------------------------------------------------
  myMQTTClient.connect()
  myMQTTClient.publish(THING_NAME + "/info", "connected", 0)
  return myMQTTClient


def AWS_MQTT_publish(MQTTClient, topic, message):
    if topic not in TOPICS:
        TOPICS.append(topic)
    #TODO Add a timestamp to the message
    MQTTClient.publish(THING_NAME + "/" + topic, message, 0)

def AWS_MQTT_Job():
    #TODO
    return

#MQTTClient = AWS_MQTT_Initialize()
