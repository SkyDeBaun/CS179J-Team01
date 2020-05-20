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

#pins for ultrasonic sensor
Trig = 11 #GPIO21
Echo = 16 #GPIO22

#Pin for led debug test
Check = 15 #GPIO3

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor1A,GPIO.OUT)
	GPIO.setup(Motor1B,GPIO.OUT)
	GPIO.setup(Motor1E,GPIO.OUT)
	GPIO.setup(Motor2A,GPIO.OUT)
	GPIO.setup(Motor2B,GPIO.OUT)
	GPIO.setup(Motor2E,GPIO.OUT)
	GPIO.setup(Trig,GPIO.OUT)
	GPIO.setup(Echo,GPIO.IN)
	GPIO.setup(Check,GPIO.OUT)

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

def sensor(Trig,Echo):
	i=0
	averageDistance=0
	for i in range(5):
		#set trig low
		GPIO.output(Trig,False)
		#delay
		time.sleep(0.1)
		#set trig to be high
		GPIO.output(Trig,True)
		time.sleep(0.00001)
		GPIO.output(Trig,False)
		#check the input from echo(sensor)
		while GPIO.input(Echo)==0:
			GPIO.output(Check,False)
		#out of loop because there was an object detected
		#send wave to be transmitted and find the time it takes to recieve signal again
		signalStart = time.time()
		while GPIO.input(Echo)==1:
			GPIO.output(Check,True)
		#loop ends done now check time
		signalEnd = time.time()
		GPIO.output(Check,False)
		#now find the distance from signals
		#find time it took from sending to receiving signal
		signalPeriod = signalEnd-signalStart
		#now calculate dist by using the speed of sound in air 17150
		distance = signalPeriod*17150
		distance = round(distance,2)
		averageDistance = averageDistance+distance
	averageDistance = averageDistance/5
	return averageDistance


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
        if humidity < 65:
                stop2()
        else:
                go2()

try:
	GPIO.setwarnings(False)
	setup()

	#AwsReyna ultrasonic connection
	myMQTTClient = AWSIoTMQTTClient("ReynaPI")
	myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
	myMQTTClient.configureCredentials("/home/pi/Certificates/rootCA.pem","/home/pi/Certificates/d626c8c838-private.pem.key","/home/pi/Certificates/d626c8c838-certificate.pem.crt")
	#myMQTTClient.configureAutoReconnectBackoffTime(1,32,20)
	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2)
	myMQTTClient.configureConnectDisconnectTimeout(10)
	myMQTTClient.configureMQTTOperationTimeout(5)
	myMQTTClient.configureAutoReconnectBackoffTime(1,32,20)

	#connect
	myMQTTClient.connect()
	distance=0
	humidity=0

	while True:

		#publish sensor data to ReynaPi/ultrasonic
		#get the timestamp
		now = datetime.utcnow()
		now_str = now.strftime('%Y-%m-%dT%H:%M%SZ')
		#get distance from ultrasonic sensor
		dis = sensor(Trig,Echo)
		payload = '{ "timestamp": "' + now_str + '","distance": ' + str(dis) + '}'
		#print(payload)
		#publish data to AWS topic ReynaPi/ultrasonic
		myMQTTClient.publish("ReynaPi/ultrasonic",payload,0)

		#subscribe to ReynaPi/ultrasonic and ryan_pi/data using callback functions
		myMQTTClient.subscribe("ReynaPi/ultrasonic",1,distCallBack)
		myMQTTClient.subscribe("ryan_pi/data",1,humidCallBack)


except KeyboardInterrupt:
		stop1()
		stop2()
		destroy()
