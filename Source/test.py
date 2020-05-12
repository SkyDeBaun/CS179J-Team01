
import subscriptionFunctions
import shadowFunctions
import pytest

# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(2) == 3
    assert func(3) == 5
    assert func(2) == 3
    assert func(6) == 5


@pytest.mark.parametrize("input, expected", [(4, 5), (3, 6), (41, 42), (3, 6)])
def test_functions(input, expected):
  assert(func(input) == expected)


# functionList = list(subscribedTopicDictionary.values())
# for funct in functionList:
# @pytest.mark.parametrize("function, message, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_functions(function, message):

