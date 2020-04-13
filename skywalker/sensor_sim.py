#import RPi.GPIO as GPIO
#import dht11
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("333052c1bf")
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("cert/rootCA.pem.crt", "cert/333052c1bf-private.pem.key", "cert/333052c1bf-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("Pi_sense01/info", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    #instance = dht11.DHT11(pin = 4) #BCM GPIO04
    result = 777 #instance.read()
    if result > 500:
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result) + ',"humidity": '+ str(9.9) + ' }'
        print (payload)
        myMQTTClient.publish("Pi_sense01/data", payload, 0)
        sleep(4)
    else:
        print (".")
        sleep(1)