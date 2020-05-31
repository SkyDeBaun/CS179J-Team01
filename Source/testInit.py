import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO

import init
import pytest
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# @pytest.mark.parametrize("argument, expectedReturn", [('c', 'c'), ('C', 'c'), ('f', 'f'), ('m', 'm'), ('r', 'r')])
# def test_parser(argument, expectedReturn):
# 	assert init.parse_args(argument) == expectedReturn

@pytest.mark.parametrize("argument, deviceType", [('c', "CameraModule"), ('f', "FanController"), ('m', "Motors"), ('r', "RadioNetwork")])
def test_init(argument, deviceType):
	assert init.initializeSystem(argument)[0].publish("TestingConnection/Topic", "connected", 0) == True and init.DEVICE_TYPE == deviceType

def init_main():
	(MQTTClient, initFunctions, stateMachine, cleanupFunction) = init.initializeSystem('t')
	output = []
	for f in initFunctions:
		output.append(f(MQTTClient))
	output.append(stateMachine(MQTTClient))
	output.append(cleanupFunction())
	return output

def test_init_main():
	assert init_main() == ["camera", "Success", "Deallocating project resources"]