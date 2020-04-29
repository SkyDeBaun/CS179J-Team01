#skys senseNet hub -> acts as interface between AWS IoT and tranceiver radios
#cs179j -> group 01 -> design project



#imports-----------------------------------------------------
#------------------------------------------------------------

#aws iot-----------------------------------------------------
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

#GPIO--------------------------------------------------------
import RPi.GPIO as GPIO

#rfm radio---------------------------------------------------
from RFM69 import Radio, FREQ_915MHZ

#utility-----------------------------------------------------
from datetime import date, datetime
import time
import json
import random
import string



#function definitions----------------------------------------
#------------------------------------------------------------

# Custom Shadow callback------------------------------------- update shadow
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("LED value: " + str(payloadDict["state"]["desired"]["LED"]))
        print("Time Stamp: " + str(payloadDict["state"]["desired"]["Time"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- delete shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- shadow Delta
def customShadowCallback_Delta(payload, responseStatus, token):
# payload is a JSON string ready to be parsed using json.loads(...)
        print("Received a message: ")
        payloadDict = json.loads(payload)
        LEDval = payloadDict["state"]["LED"] #get value from JSON field
        print ("Requested LED Value: " + str(LEDval))
        print ("Requested Time Stamp: " + payloadDict["state"]["Time"])
        print ("Token: " + str(token)) 
        print (" ")        
        #deltaMessage = json.dumps(payloadDict["state"])
        #print(deltaMessage)


# Generate unique Client_ID-----------------------------------
def generateClient_ID(stringLength = 10):
    client_string = string.ascii_letters + string.digits
    return ''.join((random.choice(client_string) for i in range(stringLength)))




#AWS IoT MQTT configuration----------------------------------
#------------------------------------------------------------

#client config----------------------------------------------- CLIENT SETTINGS
AWS_IoT_endpoint = "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com"
port = 8883
root_CA = "cert/rootCA.pem.crt"
private_key = "cert/333052c1bf-private.pem.key"
certificate = "cert/333052c1bf-certificate.pem.crt"
client_ID = generateClient_ID()
thing_name = "Pi_sense01"


# Init AWSIoTMQTTShadowClient--------------------------------
myAWSIoTMQTTShadowClient = None

#configure shadow
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(client_ID) #this can be any arbitrary string
myAWSIoTMQTTShadowClient.configureEndpoint(AWS_IoT_endpoint, port) #endpoint and port number
myAWSIoTMQTTShadowClient.configureCredentials(root_CA, private_key, certificate )#root ca and certificate used for secure connection

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thing_name, True)

#get last shadow (1 time only) - if exists (callback prints message on failure to retrieve)
deviceShadowHandler.shadowGet(customShadowCallback_Update, 5)

#update shadow on Delta (change) only
deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)


#---------------------------------------------------------------
# Update shadow in a loop---------------------------------------
loopCount = 0
while True:
    
    time.sleep(1)
