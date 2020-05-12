from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# AWS IoT certificate based connection---------------------------------------
myMQTTClient = AWSIoTMQTTClient("333052c1bf")#this can be any arbitrary string
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)#endpoint and port number
myMQTTClient.configureCredentials("Certificates/root-CA.crt", "Certificates/be178bb55c-private.pem.key","Certificates/be178bb55c-certificate.pem.crt")#root ca and certificate used for secure connection

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish----------------------------------------------------------
myMQTTClient.connect()
myMQTTClient.publish("Pi_sense01/info", "connected", 0) # #Pi_sense01 is the name of Thing on AWS IoT
 
result = 777 #read from sensor value instead (in loop below)
#----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#loop and publish sensor reading---------------------------------------------
while 1:
    now = datetime.utcnow()#iso timestamp
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    #result = 777 #read from sensor value instead
    
    if result > 500: #if result = True
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result) + ',"humidity": '+ str(99.99) + ' }'
        print (payload) #print message to console
        myMQTTClient.publish("Pi_sense01/data", payload, 0)
        sleep(5)
    else:
        print (".")
        sleep(1)
    
    result += 1
    if result > 790:
        result = 40
