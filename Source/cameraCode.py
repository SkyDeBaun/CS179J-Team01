import initializeDeviceType
import subprocess
from helpers import getTimeStamp

# def verifyCamera():
#   if initializeDeviceType.PERIPHERALS{"camera"} == 0:
#     print("Camera not connected")
#     exit(1)

def takePicture():
  fileName = "../Data/Images/" + getTimeStamp() + ".jpg"
  subprocess.run(["raspistill", "-o", fileName])

def takeVideo(duration):
  return NotImplementedError

def deletePicture():
  return NotImplementedError
