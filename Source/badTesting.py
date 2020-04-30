import functionalizedAWSIOT
import time 
MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()

functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "testing", "testing message boop beep")


while(1):
  time.sleep(2)
