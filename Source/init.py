import subprocess
import argparse
import RPi.GPIO as GPIO
import motorFunctions
import functionalizedAWSIOT



DEVICE_TYPE = None
THING_NAME = None
TOPICS = None

def initializeCameraModule(): #No hardware setup required, just checking the camera is connected
  try:
    output = subprocess.run(["/opt/vc/bin/vcgencmd", "get_camera"], universal_newlines=True, stdout=subprocess.PIPE)
    if output.stdout.find("0") :
      print("Camera not connected or not enabled")
      exit(1)
  except:
    print("Camera check only works on Raspberry Pi")
  finally:
    return

def initializeFan():
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


def intializeMotors():
	GPIO.setwarnings(False)
	motorFunctions.setup()

def parse_args(args):
  parser = argparse.ArgumentParser(description='Run the Extensible Sensor Network Project')
  flags = parser.add_mutually_exclusive_group(required=True)
  flags.add_argument('-c', '-C', help='Camera module', action='store_true')
  flags.add_argument('-f', '-F', help='Fans', action='store_true')
  flags.add_argument('-m', '-M', help='Motors', action='store_true')
  flags.add_argument('-r', '-R', help='Radio', action='store_true')
  args = vars(parser.parse_args())
  for k in args:
    if args[k]:
      return k

def initializeSystem(flag):
  global DEVICE_TYPE
  global THING_NAME
  global TOPICS
  MQTTClient = None

  if flag == 'c':
    DEVICE_TYPE = "CameraModule"
    THING_NAME = "Camera1"
    TOPICS = ["picture"]
    MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
    initializeCameraModule()
  elif flag == 'f':
    DEVICE_TYPE = "FanController"
    THING_NAME = "RyanPi"
    TOPICS = ["fan"]
    MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
    initializeFan()
    initializeTripwire(MQTTClient)
  elif flag == 'm':
    DEVICE_TYPE = "Motors"
    THING_NAME = "ReynaPi"
    TOPICS = ["ultrasonic"]
    MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
  elif flag == 'r':
    DEVICE_TYPE = "RadioNetwork"
    THING_NAME = "SkyOnAPi"
    TOPICS = ["ultrasonic"]
    MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
  else:
    print("Invalid flag check failed")
    exit(1)

  return MQTTClient

