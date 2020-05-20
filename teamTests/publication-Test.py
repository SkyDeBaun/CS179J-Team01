import RPi.GPIO as GPIO                   #Import GPIO library
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA.crt","/home/pi/AWS_certs/1aac3835be-private.pem.key","/home/pi/AWS_certs/1aac3835be-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()
payload = '{"Temperature": ' + "yessir!" +'}'
print(payload)
myMQTTClient.publish("ryanpi/data", payload, 0)
print("Data published!")
