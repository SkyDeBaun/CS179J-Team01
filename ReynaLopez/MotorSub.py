import time
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime
import json

#Pin for motor driver
Motor1A = 10 #GPIO12
Motor1B = 19 #GPIO16
Motor1E = 38 #GPIO28

Motor2A = 8
Motor2B = 21
Motor2E = 36

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor1A,GPIO.OUT)
	GPIO.setup(Motor1B,GPIO.OUT)
	GPIO.setup(Motor1E,GPIO.OUT)
	GPIO.setup(Motor2A,GPIO.OUT)
	GPIO.setup(Motor2B,GPIO.OUT)
	GPIO.setup(Motor2E,GPIO.OUT)

def go1():
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)

def stop1():
	GPIO.output(Motor1E,GPIO.LOW)

def go2():
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.HIGH)

def stop2():
	GPIO.output(Motor2E,GPIO.LOW)

def destroy():
	GPIO.cleanup()

def distCallBack(self, params,packet):
	global distance
	payloadInfo = json.loads(packet.payload)
	distance = payloadInfo["distance"]
	if distance <15:
		stop1()
	else:
		go1()

def humidCallBack(self, params, packet):
        global humidity
        payloadInfo = json.loads(packet.payload)
        humidity = payloadInfo["humidity"]
        print("humidity:", str(humidity))
        humidity = int(humidity)
        if humidity < 85:
                stop2()
        else:
                go2()

try:
	#while True:
	GPIO.setwarnings(False)
	setup()

	#AwsReyna ultrasonic connection
	myMQTTClient = AWSIoTMQTTClient("ReynaPI")
	myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
	myMQTTClient.configureCredentials("/home/pi/Certificates/rootCA.pem","/home/pi/Certificates/d626c8c838-private.pem.key","/home/pi/Certificates/d626c8c838-certificate.pem.crt")
	myMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2)
	myMQTTClient.configureConnectDisconnectTimeout(10)
	myMQTTClient.configureMQTTOperationTimeout(5)
	myMQTTClient.configureAutoReconnectBackoffTime(1,32,20)

	#connect and subscribe
	myMQTTClient.connect()
	distance=0


	while True:
		myMQTTClient.subscribe("ReynaPi/ultrasonic",1,distCallBack)
		myMQTTClient.subscribe("ryan_pi/data",1,humidCallBack)


except KeyboardInterrupt:
		stop1()
		stop2()
		destroy()
