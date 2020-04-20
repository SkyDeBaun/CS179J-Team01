#skywalker establishes basic MQTT connection for device shadow
#sends incrementing count to shadow document (with time stamp)
#based on AWS shadow publication example script




from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
from datetime import date, datetime 

import json
import RPi.GPIO as GPIO


#schema example-------------------------------------------------
# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>,
#           "property": <value, etc>,
#           "Time": <string>
#		}
#	}
# }

# Custom Shadow callback--------------------------------------
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
        print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


#callback class/function here is redundant
class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        print("Received a message: ")
        payloadDict = json.loads(payload)
        LEDval = payloadDict["state"]["LED"] #get value from JSON field
        print ("Requested LED Value: " + str(LEDval))
        print ("Requested Time Stamp: " + payloadDict["state"]["Time"])
        print ("Token: " + str(token))

        
        #deltaMessage = json.dumps(payloadDict["state"])
        #print(deltaMessage)


LEDPIN=14
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setup(LEDPIN, GPIO.OUT, initial=GPIO.LOW)

# Init AWSIoTMQTTShadowClient------------------------------------
myAWSIoTMQTTShadowClient = None

#skywalkers shadow
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("333052c1bf") #this can be any arbitrary string
myAWSIoTMQTTShadowClient.configureEndpoint("a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)#endpoint and port number
myAWSIoTMQTTShadowClient.configureCredentials("cert/rootCA.pem.crt", "cert/333052c1bf-private.pem.key", "cert/333052c1bf-certificate.pem.crt")#root ca and certificate used for secure connection

# AWSIoTMQTTShadowClient configuration

myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("Pi_sense01", True)

# Delete shadow JSON doc -> not neccesarily good for production (assuming you want to retreive data from shadow document..)
#deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) #delete first to clear existing doc

#seems reduncant -> update is providing pub/sub functionality? more testing required to verify
#shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)
#deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta) #why does it loop here? (rolled into update below?!)


#get device shadow---------------------------------------------
#deviceShadowHandler.shadowGet(customShadowCallback_Update, 5) 


#---------------------------------------------------------------
# Update shadow in a loop---------------------------------------
loopCount = 0
while True:
    deviceShadowHandler.shadowGet(customShadowCallback_Update, 5) 

    time.sleep(5)