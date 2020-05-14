import functionalizedAWSIOT
import helpers
from time import sleep
import subscriptionFunctions

def main():
#Intitialize the MQTT Client and subscriptions
  MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
#Initialize AWS access keys
  AWSCredentials = helpers.getAWSCredentials()
  print(AWSCredentials)
  subscriptionFunctions.picture(None, None, None)
  while(1):
    print("Hello World")
    sleep(5)


#functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "testing", "testing message boop beep")

if __name__ == "__main__":
  main()
