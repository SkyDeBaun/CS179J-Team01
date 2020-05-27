import subprocess
import argparse
import RPi.GPIO as GPIO



DEVICE_TYPE = None
THING_NAME = None
TOPICS = None

def initializeCameraModule():
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

def chooseDeviceType():
  global DEVICE_TYPE
  global THING_NAME
  global TOPICS

  parser = argparse.ArgumentParser(description='Run the Extensible Sensor Network Project')
  flags = parser.add_mutually_exclusive_group(required=True)
  flags.add_argument('-c', '-C', help='Camera module', action='store_true')
  flags.add_argument('-f', '-F', help='Fans', action='store_true')
  flags.add_argument('-m', '-M', help='Motors', action='store_true')
  flags.add_argument('-r', '-R', help='Radio', action='store_true')
  
  args = vars(parser.parse_args())
  print(args)
  for k in args:
    if args[k]:
      if k == 'c':
        DEVICE_TYPE = "CameraModule"
        THING_NAME = "Camera1"
        TOPICS = ["picture"]
        initializeCameraModule()
      elif k == 'f':
        DEVICE_TYPE = "FanController"
        THING_NAME = "RyanPi"
        TOPICS = ["fan"]
      elif k == 'm':
        DEVICE_TYPE = "Motors"
        THING_NAME = "ReynaPi"
        TOPICS = ["ultrasonic"]
      elif k == 'r':
        DEVICE_TYPE = "RadioNetwork"
        THING_NAME = "SkyOnAPi"
        TOPICS = ["ultrasonic"]
      else:
        print("Invalid flag check failed")
        exit(1)


chooseDeviceType()

