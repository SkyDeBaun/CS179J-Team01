
import subscriptionFunctions
import shadowFunctions

# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(2) == 3
    assert func(3) == 5
    assert func(2) == 3

