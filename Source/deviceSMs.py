from time import sleep
from datetime import date, datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import motorFunctions

def cameraSM(MQTTClient):
  print("Camera running")

def motorSM(MQTTClient):
	now = datetime.utcnow()
	now_str = now.strftime('%Y-%m-%dT%H:%M%SZ')
	dis = motorFunctions.sensor()
	payload = '{ "timestamp": "' + now_str + '","distance": ' + str(dis) + '}'
  MQTTClient.publish("ReynaPi/ultrasonic", payload, 1)
  #TODO Update to correct topic for publishing
	# functionalizedAWSIOT.AWS_MQTT_publish(myMQTTClient, "ReynaPi/ultrasonic", payload)
