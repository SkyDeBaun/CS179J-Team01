import cameraCode
import reynaPiNode
import helpers
import RPi.GPIO as GPIO
import json
from decimal import Decimal

#GUI control variable
GUI_control_fan = 0

# Should be in form customCallback(client, userdata, message)
# where message contains topic and payload.
# Note that client and userdata are here just to be aligned with the underneath Paho callback function signature.
# These fields are pending to be deprecated and should not be depended on.

def picture(client, userdata, message):
  bucketName = "senior-design-camera-files"
  try:
    fileName = cameraCode.takePicture()
    helpers.uploadToS3(fileName[0], bucketName, helpers.getAWSCredentials())
  finally:
    print("Taking picture and uploading to S3 bin")
    return True

# Function to toggle GUI's fan control (triggered from button)

def GUItoggleFanControl(client, userdata, message):
  global GUI_control_fan
  if (GUI_control_fan == 0):
    GUI_control_fan = 1
    # Turn off fan on toggle of fan control, give control of fan back to sensor
    GPIO.output(16, GPIO.HIGH)

  elif (GUI_control_fan == 1):
    GUI_control_fan = 0
    # Turn off fan on toggle of fan control, give control of fan back to sensor
    GPIO.output(16, GPIO.HIGH)


def GUIturnOnFan(client, userdata, message):
  global GUI_control_fan
  if (GUI_control_fan == 1):
    # Turn fan on
    GPIO.output(16, GPIO.LOW)

def GUIturnOffFan(client, userdata, message):
  global GUI_control_fan
  if (GUI_control_fan == 1):
    # Turn fan off
    GPIO.output(16, GPIO.HIGH)

def controlFan(client, userdata, message):
  global GUI_control_fan

  payloadDict = json.loads(message.payload)
  humidity = Decimal(payloadDict["humidity"])

  # Note GUI_control_fan in conditionals
  if (humidity > 85 and GUI_control_fan == 0):
    # Turning fan on
    GPIO.output(16, GPIO.LOW)
    return 1

  elif (humidity <= 85 and GUI_control_fan == 0):
    # Turning fan off
    GPIO.output(16, GPIO.HIGH)
    return 0


def data(self, params, packet):
  print("")

def ultrasonic(client, userdate, message):
  distance=0
  payloadInfo = json.loads(message.payload)
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
  "controlFan" : controlFan,
  "ultrasonic" : ultrasonic,
  "motor2" : motor2,
  "GUItoggleFanControl" : GUItoggleFanControl,
  "GUIturnOnFan" : GUIturnOnFan,
  "GUIturnOffFan" : GUIturnOffFan,
  "data" : data
  #FIXME Find some way to not hardcode value names
}


#https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
#Maybe check if k is valid input
def generateCallbackFunction(k):
  return subscribedTopicDictionary[k]

