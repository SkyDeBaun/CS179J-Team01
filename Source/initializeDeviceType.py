import subprocess

#Make negative or positive enabling based on other tests to determine if sensors are present
PERIPHERALS = {"camera" : 0, "tripwire" : 0, "motor" : 0, "ultrasonic" : 0, "fan" : 0, "temperature" : 0, "humidity" : 0}

def checkCamera():
  output = subprocess.run(["/opt/vc/bin/vcgencmd", "get_camera"], universal_newlines=True, stdout=subprocess.PIPE)
  if output.stdout.find("0") :
    PERIPHERALS["camera"] = 0
  else:
    PERIPHERALS["camera"] = 1
