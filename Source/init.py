DEVICE_TYPE = "InitialValueForTesting"
THING_NAME = "InitialValueForTesting"
TOPICS = ["picture"]
import sys
import subprocess
import argparse
import RPi.GPIO as GPIO
import motorFunctions
import functionalizedAWSIOT

import deviceSMs
import cleanup

def initializeCameraModule(myMQTTClient): #No hardware setup required, just checking the camera is connected
  try:
    output = subprocess.run(["/opt/vc/bin/vcgencmd", "get_camera"], universal_newlines=True, stdout=subprocess.PIPE)
    if output.stdout.find("0") :
      print("Camera not connected or not enabled")
      exit(1)
  except:
    print("Camera check only works on Raspberry Pi")
  finally:
    return "camera"

def initializeFan(myMQTTClient):
  # Setup pins
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  # Specifiy the pin that will control the DC fan
  GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)
  GPIO.output(16, GPIO.HIGH)

def initializeTripwire(myMQTTClient):
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  #TODO Write the "event" function to publish

  def triggeredWire(ev=None):
    myMQTTClient.publish("CameraModule/Camera1/picture", "Wire tripped", 0)
  
  GPIO.add_event_detect(21, GPIO.FALLING, callback=triggeredWire, bouncetime=5000)


def intializeMotors(myMQTTClient):
	GPIO.setwarnings(False)
	motorFunctions.setup()

def parse_args(args):
  parser = argparse.ArgumentParser(description='Run the Extensible Sensor Network Project')
  flags = parser.add_mutually_exclusive_group(required=True)
  flags.add_argument('-c', '-C', help='Camera module', action='store_true')
  flags.add_argument('-f', '-F', help='Fans', action='store_true')
  flags.add_argument('-m', '-M', help='Motors', action='store_true')
  flags.add_argument('-r', '-R', help='Radio', action='store_true')
  flags.add_argument('-t', '-T', help='Testing', action='store_true') #FIXME Comment out before production 

  arguments = vars(parser.parse_args(args))
  for k in arguments:
    if arguments[k]:
      print(k)
      return k

def initializeSystem(flag):
  global DEVICE_TYPE
  global THING_NAME
  global TOPICS
  INIT_FUNCTIONS = []
  STATE_MACHINE = None
  CLEANUP_FUNCTION = cleanup.emptyCleanup
  MQTTClient = None

  if flag == 'c':
    DEVICE_TYPE = "CameraModule"
    THING_NAME = "Camera1"
    TOPICS = ["picture"]
    INIT_FUNCTIONS = [initializeCameraModule]
    STATE_MACHINE = deviceSMs.cameraSM
    CLEANUP_FUNCTION = cleanup.emptyCleanup
  elif flag == 'f':
    DEVICE_TYPE = "FanController"
    THING_NAME = "RyanPi"
    TOPICS = ["fan"]
    INIT_FUNCTIONS = [initializeFan, initializeTripwire]
  elif flag == 'm':
    DEVICE_TYPE = "Motors"
    THING_NAME = "ReynaPi"
    TOPICS = ["ultrasonic"]
    INIT_FUNCTIONS = [intializeMotors]
    STATE_MACHINE = deviceSMs.motorSM
    CLEANUP_FUNCTION = cleanup.cleanMotors
  elif flag == 'r':
    DEVICE_TYPE = "RadioNetwork"
    THING_NAME = "SkyOnAPi"
    TOPICS = ["ultrasonic"]
  elif flag == 't':
    DEVICE_TYPE = "testing"
    THING_NAME = "testing"
    TOPICS = ["camera"]
    INIT_FUNCTIONS = [initializeCameraModule]
    STATE_MACHINE = deviceSMs.SMtest
    CLEANUP_FUNCTION = cleanup.emptyCleanup
  else:
    print("Invalid flag check failed")
    exit(1)
  MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
  return (MQTTClient, INIT_FUNCTIONS, STATE_MACHINE, CLEANUP_FUNCTION)

# if __name__ == "__main__":
#   parse_args(sys.argv[1:])