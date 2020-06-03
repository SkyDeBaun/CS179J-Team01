import sys
import fake_rpi
import fake_radio


sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['RFM69'] = fake_radio.Radio


import subscriptionFunctions
import pytest
import functionalizedAWSIOT
import helpers
from time import sleep

def main_func():
  MQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
  if functionalizedAWSIOT.AWS_MQTT_subscribe(MQTTClient, "testing", subscriptionFunctions.testCallbackFunction):
    sleep(5)
    functionalizedAWSIOT.AWS_MQTT_publish(MQTTClient, "testing", "testing message boop beep")
    sleep(5)
    return subscriptionFunctions.GLOBAL_TEST_VARIABLE
  return -1

def test_Travis():
  assert main_func() > 0
