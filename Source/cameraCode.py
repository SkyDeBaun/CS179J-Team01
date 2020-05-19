import initializeDeviceType
import subprocess
from helpers import getTimeStamp

# def verifyCamera():
#   if initializeDeviceType.PERIPHERALS{"camera"} == 0:
#     print("Camera not connected")
#     exit(1)

def takePicture():
  fileName = getTimeStamp() + ".jpg"
  filePath = "../Data/Images/" + fileName
  try:
    subprocess.run(["raspistill","-n","-t", "1", "-o", filePath])
    #See if this is blocking
  except:
    print("Camera not connected")
    return (filePath, fileName) #Tuple in case I see future use to have standalone file name and path

def takeVideo(duration):
  return NotImplementedError

def deletePicture():
  return NotImplementedError
