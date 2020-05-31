from time import sleep
from datetime import date, datetime
import functionalizedAWSIOT
import motorFunctions

def cameraSM(MQTTClient):
  print("Camera running")

def motorSM(MQTTClient):
	now = datetime.utcnow()
	now_str = now.strftime('%Y-%m-%dT%H:%M%SZ')
	dis = motorFunctions.sensor()
	payload = '{ "timestamp": "' + now_str + '","distance": ' + str(dis) + '}'
  #TODO Update to correct topic for publishing
	functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "ReynaPi/ultrasonic", payload)


def SMtest(MQTTClient):
  if functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "testing", "testing state machine"):
    return "Success"
