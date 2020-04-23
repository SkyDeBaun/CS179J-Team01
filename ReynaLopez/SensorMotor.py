import time
import RPi.GPIO as GPIO

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
	 print("check sensor ")
         #set trig low 
         GPIO.output(Trig,False)
         print("set trig out false")
	 #delay
         time.sleep(0.1)
         #set trig to be high
         GPIO.output(Trig,True)
         print("set trig true")
         time.sleep(0.00001)
         GPIO.output(Trig,False)
         print("set trig false next")
         #check the input from echo(sensor)
         while GPIO.input(Echo)==0:
		#print("no input from echo")
		#if no input to echo the debug light is off
                GPIO.output(Check,False)
         #out of loop because got an input from echo
         signalStart = time.time()
         while GPIO.input(Echo)==1:
                print("got input from echo")
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
        averageDistance = averageDistance/4
        print("Distance: %.1f cm" % averageDistance)
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
        try:
                i=0
		dis=0
		go()
                for i in range(10):
			dis = sensor(Trig1,Echo1)
                        if dis<15 :
				print("stop motor to close")
				stop()
                        else:
				go()
                stop()
		exit()

        except KeyboardInterrupt:
		stop()
		destroy()
