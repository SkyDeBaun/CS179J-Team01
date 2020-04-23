import time 
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime

#Pin for motor driver
Motor1A = 10 #GPIO12 
Motor1B = 19 #GPIO16
Motor1E = 38 #GPIO28

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor1A,GPIO.OUT)
	GPIO.setup(Motor1B,GPIO.OUT)
   	GPIO.setup(Motor1E,GPIO.OUT)
def go():
	GPIO.output(Motor1A,GPIO.HIGH) 
	GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)

def stop():
	GPIO.output(Motor1E,GPIO.LOW)

def destroy():
	GPIO.cleanup()

def on_publish(self, params,packet):
	print(packet.payload)

if __name__ == '__main__':

	GPIO.setwarnings(False)
        setup()

        #AwsReyna connection
        myMQTTClient = AWSIoTMQTTClient("ReynaPI")
        myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-east-2.amazonaws.com",8883)
	myMQTTClient.configureCredentials("/home/pi/SeniorPrj/cert/RootCA.pem","/home/pi/SeniorPrj/cert/e69f767736-private.pem.key","/home/pi/SeniorPrj/cert/e69f767736-certificate.pem.crt")
        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(10)
        myMQTTClient.configureMQTTOperationTimeout(5)
	myMQTTClient.configureAutoReconnectBackoffTime(1,32,20)

        #connect and subscribe
        myMQTTClient.connect()
	myMQTTClient.subscribe("ReynaPi/ultrasonic",1,on_publish)

	try:
		while True:
			dis = on_publish
			if dis<15:
				stop()
			else:
				go()

	except KeyboardInterrupt:
		stop()
		destroy()
