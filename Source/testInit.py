import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO

import init
import pytest
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

@pytest.mark.parametrize("argument, expectedReturn", [('-c', 'c'), ('-C', 'c'), ('-f', 'f'), ('-m', 'm'), ('-r', 'r')])
def test_parser(argument, expectedReturn):
	assert init.parse_args(argument) == expectedReturn

@pytest.mark.parametrize("argument, deviceType", [('c', "CameraModule"), ('f', "FanController"), ('m', "Motors"), ('r', "RadioNetwork")])
def test_parser(argument, deviceType):
	assert init.initializeSystem(argument).publish("TestingConnection/Topic", "connected", 0) == True
  assert init.DEVICE_TYPE == deviceType