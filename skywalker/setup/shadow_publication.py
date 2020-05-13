#skywalker establishes basic MQTT publication for device shadow
#sends incrementing count to shadow document (with time stamp)
#based on AWS shadow publication example script




from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
from datetime import date, datetime
import json

#schema example-------------------------------------------------
# Shadow JSON schema:
#
# Name: Bot
# {
#	"state": {
#		"desired":{
#			"property":<INT VALUE>,
#           "LED": <value, etc>,
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


#delta callback--------------------------------------------------
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



# Init AWSIoTMQTTShadowClient------------------------------------
myAWSIoTMQTTShadowClient = None

#skywalkers shadow
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("zc1bf") #this can be any UNIQUE string (for testing with same Thing.. use different client ID's!!!)
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

# Delete device shodow------------------------------------------
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) #delete first to clear existing doc

#Delta Callback-------------------------------------------------
#shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)
#deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta) #why does it loop here? (rolled into update below?!)


#---------------------------------------------------------------
# Update shadow in a loop---------------------------------------
loopCount = 0
while True:

    #publish data to device shadow------------------------------
    now = datetime.utcnow()#iso timestamp
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    JSONPayload = '{"state":{"desired":{"property":' + str(loopCount) + ', "LED": '+ str(2 * loopCount) + ', "Time": "' + now_str + '"}}}'
    deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5) #5 is token setting (?)
    loopCount += 1
    time.sleep(5)