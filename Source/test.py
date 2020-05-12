
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

functionList = list(subscriptionFunctions.subscribedTopicDictionary.values())
functionList.append(print)

@pytest.mark.parametrize("function", functionList)
def test_publishFunctionSignatures(function):
  assert len(inspect.signature(function).parameters) == 3