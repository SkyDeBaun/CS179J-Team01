import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO


import subscriptionFunctions
import shadowFunctions
import pytest #My local machine doesn't like this
import inspect
import json

# content of test_sample.py
# def func(x):
#     return x + 1

# @pytest.mark.parametrize("input, expected", [(4, 5), (3, 6), (41, 42), (3, 6)])
# def test_functions(input, expected):
#   assert(func(input) == expected)


#################################################################################
# Template parametrized test function 
# All capitalized letter words are where things need to be filled in
# The name of test should have "test_" affixiated to the front
# INPUT and EXPECTED are automatically filled in in the function call with the items from the list
# @pytest.mark.parametrize("INPUT, EXPECTED, ANY_ADDITIONAL_PARAMETERS_THAT_MAY_CHANGE", [(FIRST_INPUT_VALUE, FIRST_EXPECTED_VALUE), (SECOND_INPUT_VALUE, SECOND_EXPECTED_VALUE)])
# def NAME_OF_TEST_FUNCTION(INPUT, EXPECTED):
#   assert(CALLBACK_FUNCTION(None, None, INPUT) == EXPECTED)
#
# Example if value is greater than 15
# @pytest.mark.parametrize("data, expectedStatus", [(25, True), (10, False), (1000, True), (1, False), (15, False)])
# def test_greaterThan15(INPUT, EXPECTED):
#   assert(greaterThan15(None, None, data) == expectedStatus)
#
#################################################################################

functionList = list(subscriptionFunctions.subscribedTopicDictionary.values()) #Get the list of all callback functions

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions have the proper signature
def test_publishFunctionSignatures(function):
  assert len(inspect.signature(function).parameters) == 3

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions are implemented
def test_publishFunctionSignatures(function):
  assert function(None, None, "test payload") != NotImplemented

#test values for motor test messages as jsons
data1 = {"distance":25, "humidity":83}
message1 = json.dump(data1)
data2 = {"distance":10, "humidity":62}
message2 = json.dump(data2)
data3 = {"distance":100, "humidity":98}
message3=json.dump(data3)
data4 = {"distance":7, "humidity":30}
message4 = json.dump(data4)

@pytest.mark.parametrize("message", "expectedStatus", [(message1, 1), (message2, 0), (message3, 1), (message4, 0)])
def test_motorOperationBehaviour(message, expectedStatus):
	assert subscriptionFunctions.subscribedTopicDictionary["ultrasonic"](None, None, message) == expectedStatus

@pytest.mark.parametrize("message", "expectedStatus", [(message1, 1), (message2, 0), (message3, 1), (message4, 0)])
def test_motor2OperationBehaviour(message, expectedStatus):
  assert subscriptionFunctions.subscribedTopicDictionary["motor2"](None, None, message) == expectedStatus

