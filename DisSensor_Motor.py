import time 
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime

#Pin for ultrasonic sensor
Trig1 = 11 #GPIO21 
Echo1 = 16 #GPIO22

#Pin for motor driver
Motor1A = 10 #GPIO12
Motor1B = 19 #GPIO16
Motor1E = 38 #GPIO28

#Pin for led debugg test
Check = 15 #GPIO3 

def setup():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(Trig1,GPIO.OUT)
   GPIO.setup(Echo1,GPIO.IN)
   GPIO.setup(Check,GPIO.OUT)
   GPIO.setup(Motor1A,GPIO.OUT)
   GPIO.setup(Motor1B,GPIO.OUT)
   GPIO.setup(Motor1E,GPIO.OUT)

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
		#print("no input from echo") if no input to echo the debug light 
		#is off
                GPIO.output(Check,False)
              #out of loop because got an input from echo
              signalStart = time.time()
	      while GPIO.input(Echo)==1:
	        # print("got input from echo")
		#when theres an input turn light on (debugging/testing)
		GPIO.output(Check,True)
	      #loop ends so input done now check time
	      signalEnd = time.time()
	      GPIO.output(Check,False)
   	      #now find the distance from signals input
              signalPeriod = signalEnd-signalStart
	      distance = signalPeriod*17150
              #print("found distance ")
              distance = round(distance,2)
	      averageDistance = averageDistance+distance
         averageDistance = averageDistance/5
	 return averageDistance

def go():
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)

def stop():
	 GPIO.output(Motor1E,GPIO.LOW)

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':

	GPIO.setwarnings(False)
	setup()

	#Aws Iot based connection
	myMQTTClient = AWSIoTMQTTClient("ID")
	myMQTTClient.configureEndpoint("a31m7pjtvk0tgd-ats.iot.us-east-2.amazonaws.com",8883)
	myMQTTClient.configureCredentials("/home/pi/SeniorPrj/Certificates/RootCA.pem","/home/pi/SeniorPrj/Certificates/600bce1b0c-private.pem.key","/home/pi/SeniorPrj/Certificates/600bce1b0c-certificate.pem.crt")
	myMQTTClient.configureOfflinePublishQueueing(-1)
	myMQTTClient.configureDrainingFrequency(2)
	myMQTTClient.configureConnectDisconnectTimeout(10)
	myMQTTClient.configureMQTTOperationTimeout(5)

	#connect and publish the connection
	myMQTTClient.connect()
	myMQTTClient.publish("pi/info", "connected", 0)

	try:
	 	while 1:
			dis = sensor(Trig1,Echo1)
               		if dis<15 :
			 	 stop()
				 now = datetime.utcnow()
				 now_str = now.strftime('%Y-%m-%dT%H:%M%SZ')
				 payload = '{ "timestamp": "' + now_str + '","distance": ' + str(dis) + '}'
				 print(payload)
				 myMQTTClient.publish("pi/data",payload,0)
			else:
				 go()

        except KeyboardInterrupt: 
		stop()
		destroy()
