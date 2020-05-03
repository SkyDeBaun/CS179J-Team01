import time
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime

#pins for ultrasonic sensor
Trig = 11 #GPIO21
Echo = 16 #GPIO22

#Pin for led debug test
Check = 15 #GPIO3

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Trig,GPIO.OUT)
	GPIO.setup(Echo,GPIO.IN)
	GPIO.setup(Check,GPIO.OUT)

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

GPIO.setwarnings(False)
setup()

#AwsReyna connection
myMQTTClient = AWSIoTMQTTClient("ReynaPI")
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com",8883)
myMQTTClient.configureCredentials("/home/pi/SeniorPrj/reynaPiCerts/rootCA.pem","/home/pi/SeniorPrj/reynaPiCerts/d626c8c838-private.pem.key","/home/pi/SeniorPrj/reynaPiCerts/d626c8c838-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

#connect and publish the connection
myMQTTClient.connect()

while True:
		#get the timestamp
		now = datetime.utcnow()
		now_str = now.strftime('%Y-%m-%dT%H:%M%SZ')
		#get distance from ultrasonic sensor
		dis = sensor(Trig,Echo)
		payload = '{ "timestamp": "' + now_str + '","distance": ' + str(dis) + '}'
		print(payload)
		#publish data to AWS topic ReynaPi/ultrasonic
		myMQTTClient.publish("ReynaPi/ultrasonic",payload,0)
