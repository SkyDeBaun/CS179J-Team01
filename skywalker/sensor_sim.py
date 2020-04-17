#Skywalker connects Raspberry Pi to AWS IoT Core -> Happy Easter
#2048 bit encrypted MQTT messaging protocol 
#publishes payload -> a json object (w/static test values)

#includes--------------------------------------------------------------------
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime 
 
# AWS IoT certificate based connection---------------------------------------
myMQTTClient = AWSIoTMQTTClient("333052c1bf")#this can be any arbitrary string
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)#endpoint and port number
myMQTTClient.configureCredentials("cert/rootCA.pem.crt", "cert/333052c1bf-private.pem.key", "cert/333052c1bf-certificate.pem.crt")#root ca and certificate used for secure connection

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish----------------------------------------------------------
myMQTTClient.connect()
myMQTTClient.publish("Pi_sense01/info", "connected", 0) # #Pi_sense01 is the name of Thing on AWS IoT
 
# Create a device shadow handler, use this to update and delete shadow document
#deviceShadowHandler = myMQTTClient.createShadowHandlerWithName(Pi_sense01, True)

# Delete current shadow JSON doc
#deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)



#----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#loop and publish sensor reading---------------------------------------------
while 1:
    now = datetime.utcnow()#iso timestamp
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    result = 777 #read from sensor value instead
    if result > 500: #if result = True
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result) + ',"humidity": '+ str(99.99) + ' }'
        print (payload) #print message to console
        #myMQTTClient.publish("Pi_sense01/data", payload, 0) #Pi_sense01 is the name of Thing on AWS IoT
        myMQTTClient.publish("Pi_sense01/data", payload, 0)
        #deviceShadowHandler.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 5)
        sleep(5)
    else:
        print (".")
        sleep(1)
