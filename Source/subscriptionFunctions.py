import cameraCode
import MotorSub
import json

# Should be in form customCallback(client, userdata, message)
# where message contains topic and payload. 
# Note that client and userdata are here just to be aligned with the underneath Paho callback function signature.
# These fields are pending to be deprecated and should not be depended on.

def picture(client, userdata, message):#TODO Implement callback funcitonality
  cameraCode.takePicture()
  #TODO something about s3 upload
  return

def stream(client, userdata, message):#TODO Implement callback functionality
  return NotImplementedError

def video(client, userdata, message):#TODO Implement callback functionality
  return NotImplementedError

def ultrasonic(client, userdate, message):
  distance=0
  payloadInfo = json.load(message.payload)
  distance = payloadInfo["distance"]
  if distance<15:
    MotorSub.stop()
  else:
    MotorSub.go()

subscribedTopicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video,
  "ReynaPi/ultrasonic" " : ReynaPi/ultrasonic
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]
