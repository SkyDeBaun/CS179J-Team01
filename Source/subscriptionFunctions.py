import cameraCode
import helpers

# Should be in form customCallback(client, userdata, message)
# where message contains topic and payload. 
# Note that client and userdata are here just to be aligned with the underneath Paho callback function signature.
# These fields are pending to be deprecated and should not be depended on.

def picture(client, userdata, message):#TODO Implement callback funcitonality
  bucketName = "senior-design-camera-files"
  fileName = cameraCode.takePicture()
  try:
    helpers.uploadToS3(fileName[0], bucketName, helpers.getAWSCredentials())
  finally:
    print("Taking picture and uploading to S3 bin")
    return True

def stream(client, userdata, message):#TODO Implement callback functionality
  return NotImplemented

def video(client, userdata, message):#TODO Implement callback functionality
  return NotImplemented

subscribedTopicDictionary = {
  "picture" : picture,
  "stream" : stream,
  "video" : video
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]
