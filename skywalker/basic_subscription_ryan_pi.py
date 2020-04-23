#Skywalker establishes basic MQTT subscription
#2048 bit encrypted MQTT messaging protocol 

#includes--------------------------------------------------------------------
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import date, datetime
import json


Device_ID = "Pi_sense01"

# AWS IoT certificate based connection---------------------------------------
myMQTTClient = AWSIoTMQTTClient(Device_ID)#this can be any arbitrary string
myMQTTClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)#endpoint and port number
myMQTTClient.configureCredentials("cert/rootCA.pem.crt", "cert/333052c1bf-private.pem.key", "cert/333052c1bf-certificate.pem.crt")#root ca and certificate used for secure connection

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish----------------------------------------------------------
myMQTTClient.connect()
Temp = 0


 # Callback function triggered when the topic subscribed to gets new published data
def myCallBack(self, params, packet):
        #print(packet.payload)
        payloadDict = json.loads(packet.payload)
        global Temp
        Temp = payloadDict ["temperature"] #get value from JSON field
        Humidity = payloadDict["humidity"] #get value
        print("Temperature: " + str(Temp))
        print("Humidity: " + str(Humidity))
        print(" ")

        if Humidity > 85.0:
            print ("HIGH HUMIDITY THRESHOLD***************************")






# Specify what to do, when we receive an update-------------------------------- for future reference
'''
def callback_update_accepted(Device_ID, userdata, message):
    print("Got an update, on the topic:")
    print(str(message.topic))
    print("The message is this")
    print(str(message.payload))

# Specify what to do, when the update is rejected
def callback_update_rejected(Device_ID, userdata, message):
    print("The update was rejected. Received the following message:")
    print(str(message.payload))
'''

# Subscribe--------------------------------------------------------------------
print("Subscribing...")

#alt methods(?)---------------------------------------------------------------- for future reference
#myMQTTClient.subscribe(topic_update + "/accepted", 1, callback_update_accepted)
#time.sleep(2)
#myMQTTClient.subscribe(topic_update + "/rejected", 1, callback_update_rejected)
#time.sleep(2)

myMQTTClient.subscribe("ryan_pi/data", 1, myCallBack)
print("...")


#----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#loop and publish sensor reading---------------------------------------------
while 1:
    

    time.sleep(3)