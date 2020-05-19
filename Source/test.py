
import subscriptionFunctions
import shadowFunctions
import pytest #My local machine doesn't like this
import inspect

# content of test_sample.py
# def func(x):
#     return x + 1

# @pytest.mark.parametrize("input, expected", [(4, 5), (3, 6), (41, 42), (3, 6)])
# def test_functions(input, expected):
#   assert(func(input) == expected)


#################################################################################
# Example parametrized test function 
# All capitalized letter words are where things need to be filled in
# @pytest.mark.parametrize("INPUT, EXPECTED, ANY_ADDITIONAL_PARAMETERS_THAT_MAY_CHANGE", [(FIRST_INPUT_VALUE, FIRST_EXPECTED_VALUE), (SECOND_INPUT_VALUE, SECOND_EXPECTED_VALUE)])
# The name of test should have "test_" affixiated to the front
# def NAME_OF_TEST_FUNCTION(INPUT, EXPECTED):
#   assert(CALLBACK_FUNCTION(None, None, INPUT) == EXPECTED)
#
#
#
#################################################################################

functionList = list(subscriptionFunctions.subscribedTopicDictionary.values()) #Get the list of all callback functions

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions have the proper signature
def test_publishFunctionSignatures(function):
  assert len(inspect.signature(function).parameters) == 3

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions are implemented
def test_publishFunctionSignatures(function):
  assert function(None, None, "test payload") != NotImplemented

@pytest.mark.parametrize("message", "expectedStatus", [("", 1), ("", 0), ("", 1), ("", 0)]) #1 or 0 output from the ultrasonic callback function. Put the inputs in quotes
def test_motorOperationBehaviour(message, expectedStatus):
  #TODO Reyna
  assert subscriptionFunctions.subscribedTopicDictionary["ultrasonic"](None, None, message) == expectedStatus
