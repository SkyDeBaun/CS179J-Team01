import cameraCode
import reynaPiNode
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
    reynaPiNode.stop1()
    return 0
  else:
    reynaPiNode.go1()
    return 1

def motor2(client, userdate, message):
  humidity=0
  payloadInfo = json.loads(message.payload)
  humidity = payloadInfo["humidity"]
  print("humidity:", str(humidity))
  humidity = int(humidity)
  if humidity < 65:
   reynaPiNode.stop2()
   return 0
  else:
   reynaPiNode.go2()
   return 1

subscribedTopicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video,
  "ultrasonic" : ultrasonic,
  "motor2" : motor2
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]
