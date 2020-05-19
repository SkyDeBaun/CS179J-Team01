import cameraCode
import helpers
import RPi.GPIO as GPIO
import json
from decimal import Decimal

# Should be in form customCallback(client, userdata, message)
# where message contains topic and payload. 
# Note that client and userdata are here just to be aligned with the underneath Paho callback function signature.
# These fields are pending to be deprecated and should not be depended on.

def picture(client, userdata, message):#TODO Implement callback funcitonality
  bucketName = "senior-design-camera-files"
  fileName = cameraCode.takePicture()
  helpers.uploadToS3(fileName[0], bucketName, helpers.getAWSCredentials())
  #TODO something about s3 upload
  print("Taking picture and uploading to S3 bin")
  return

def stream(client, userdata, message):#TODO Implement callback functionality
  return NotImplementedError

def video(client, userdata, message):#TODO Implement callback functionality
  return NotImplementedError

def controlFan(self, params, packet):
  payloadDict = json.loads(packet.payload)
  humidity = Decimal(payloadDict["humidity"])
  print(packet.payload)
  if (humidity > 85):
    print("Fan is ON")
    print("####")
    GPIO.output(16, GPIO.LOW)
    fanOn = True

  else:
    print("Fan is OFF")
    print("####")
    GPIO.output(16, GPIO.HIGH)
    fanOn = False


subscribedTopicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video, 
  "controlFan" : controlFan
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]
