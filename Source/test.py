
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

functionList = list(subscriptionFunctions.subscribedTopicDictionary.values())
functionList.append(print)

@pytest.mark.parametrize("function", functionList)
def test_publishFunctionSignatures(function):
  assert len(inspect.signature(function).parameters) == 3

data = {"distance":25}
message = json.dump(data)
expectedStatus = 1

@pytest.mark.parametrize("message", "expectedStatus", [("", 1), ("", 0), ("", 1), ("", 0)])
def test_motorOperationBehaviourGO(message, expectedStatus):
	assert subscriptionFunctions.subscribedTopicDictionary["ultrasonic"](None, None, message) == expectedStatus

data = {"distance":15}
message = json.dump(data)
expectedStatus = 0
def test_motorOperationBehaviorStop(message,expectedStatus):
	assert subscriptionFunctions.subscribedTopicDictionart["ultrasonic"](None, None, message)== expectedStatus
