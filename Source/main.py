import sys
import init
import functionalizedAWSIOT
import helpers
from time import sleep
import subscriptionFunctions

def main():
#Intitialize the MQTT Client and subscriptions
  MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
#Initialize AWS access keys
  AWSCredentials = helpers.getAWSCredentials()
#  print(AWSCredentials)
  #subscriptionFunctions.picture(None, None, None)
  while(1):
    sleep(5)



def newMain():
  input = init.parse_args(sys.argv[1:])
  print(input)
  (MQTTClient, initFunctions, stateMachine, cleanupFunction) = init.initializeSystem(input)
  for f in initFunctions:
    f(MQTTClient)

  try:
    while 1:
      stateMachine()
      sleep(3)

  finally:
    cleanupFunction()
#functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "testing", "testing message boop beep")

if __name__ == "__main__":
  main()
