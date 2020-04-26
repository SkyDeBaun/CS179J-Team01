import subprocess

#Make negative or positive enabling based on other tests to determine if sensors are present
peripherals = {"camera" : 0, "tripwire" : 0, "motor" : 0, "ultrasonic" : 0, "fan" : 0, "temperature" : 0, "humidity" : 0}

output = subprocess.run(["/opt/vc/bin/vcgencmd", "get_camera"], universal_newlines=True, stdout=subprocess.PIPE)
if output.stdout.find("0") :
  peripherals["camera"] = 0
else:
  peripherals["camera"] = 1
