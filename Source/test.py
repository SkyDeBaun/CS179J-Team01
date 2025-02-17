import sys
import fake_rpi
import fake_radio

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['RFM69'] = fake_radio.Radio


import subscriptionFunctions
import shadowFunctions
import pytest #My local machine doesn't like this
import inspect
import json
import time
from dynamoDBFunctions import createTable
from dynamoDBFunctions import deleteTable
from dynamoDBFunctions import insertRow
import boto3
import string
import random

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

#Mock class for packet
class message:
  payload = None
  topic = None

  def __init__(self, payload):
    self.payload = payload

functionList = list(subscriptionFunctions.subscribedTopicDictionary.values()) #Get the list of all callback functions

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions have the proper signature
def test_publishFunctionSignatures(function):
  assert len(inspect.signature(function).parameters) == 3

@pytest.mark.parametrize("function", functionList) #Tests that the callback functions are implemented
def test_implementedCallbacks(function):
  assert function("Testing", "Testing", message('{ "temperature": ' + "20" + ',"humidity": '+ "50" + ',"distance": ' + "20"  ', "Temperature": "21.21", "Light": "72" }')) != NotImplemented

# test values for motor test messages as jsons
message1 = message('{ "distance": ' + "25" + ',"humidity": '+ "83" + ' }')
message2 = message('{ "distance": ' + "10" + ',"humidity": '+ "62" + ' }')
message3 = message('{ "distance": ' + "100" + ',"humidity": '+ "98" + ' }')
message4 = message('{ "distance": ' + "7" + ',"humidity": '+ "30" + ' }')

@pytest.mark.parametrize("message, expectedStatus", [(message1, 1), (message2, 0), (message3, 1), (message4, 0)])
def test_motorOperationBehaviour(message, expectedStatus):
	assert subscriptionFunctions.subscribedTopicDictionary["ultrasonic"](None, None, message) == expectedStatus

@pytest.mark.parametrize("message, expectedStatus", [(message1, 1), (message2, 0), (message3, 1), (message4, 0)])
def test_motor2OperationBehaviour(message, expectedStatus):
 assert subscriptionFunctions.motor2("Testing", "Testing", message) == expectedStatus

#Tests for DC fan below (radio callback test borrows this as well)

#Test data
data1 = '{ "temperature": ' + "20" + ',"humidity": '+ "50" + ' }'
data2 = '{ "temperature": ' + "40" + ',"humidity": '+ "100" + ' }'
data3 = '{ "temperature": ' + "15" + ',"humidity": '+ "86" + ' }'
data4 = '{ "temperature": ' + "99" + ',"humidity": '+ "84" + ' }'
message1 = message(data1)
message2 = message(data2)
message3 = message(data3)
message4 = message(data4)

@pytest.mark.parametrize("message, expectedStatus", [(message1, 0), (message2, 1), (message3, 1), (message4, 0)])
def test_fanOperational(message, expectedStatus):
  assert subscriptionFunctions.controlFan("Testing", "Testing", message) == expectedStatus


#radio function test -> uses Test data from above (also)---------
@pytest.mark.parametrize("message, expectedStatus", [(message1, 0), (message3, 1)])
def test_subHumiture(message, expectedStatus):
  assert subscriptionFunctions.subscribedTopicDictionary["subHumiture"](None, None, message) == expectedStatus

# Tests for GUI triggered callback functions

def test_GUIturnOnFan_enabled():
  assert subscriptionFunctions.GUIturnOnFan("Test enabled", "Test enabled", None) == 1

def test_GUIturnOnFan_disabled():
  assert subscriptionFunctions.GUIturnOnFan("Test disabled", "Test disabled", None) == 0

def test_GUIturnOffFan_enabled():
  assert subscriptionFunctions.GUIturnOffFan("Test enabled", "Test enabled", None) == 1

def test_GUIturnOffFanControl_disabled():
  assert subscriptionFunctions.GUIturnOffFan("Test disabled", "Test disabled", None) == 0

def test_GUItoggleFanControl_toggleOn():
  assert subscriptionFunctions.GUItoggleFanControl("Toggle on", "Toggle on", None) == 1

def test_GUItoggleFanControl_toggleOff():
  assert subscriptionFunctions.GUItoggleFanControl("Toggle off", "Toggle off", None) == 0

def test_GUIturnOnMotor_enabled():
  assert subscriptionFunctions.GUIturnOnMotor("Test enabled", "Test enabled", None) == 1

def test_GUIturnOnMotor_disabled():
  assert subscriptionFunctions.GUIturnOnMotor("Test disabled", "Test disabled", None) == 0

def test_GUIturnOffMotor_enabled():
  assert subscriptionFunctions.GUIturnOffMotor("Test enabled", "Test enabled", None) == 1

def test_GUIturnOffMotorControl_disabled():
  assert subscriptionFunctions.GUIturnOffMotor("Test disabled", "Test disabled", None) == 0

def test_GUItoggleMotorControl_toggleOn():
  assert subscriptionFunctions.GUItoggleMotorControl("Toggle on", "Toggle on", None) == 1

def test_GUItoggleMotorControl_toggleOff():
  assert subscriptionFunctions.GUItoggleMotorControl("Toggle off", "Toggle off", None) == 0



# Test createTable() function for DynamoDB using createTable() function from temperatureHumidity.py
#def test_createDynamoTable():
#  tableName = "tableToCreateThenDelete"
#  primaryColumnName = "testPrimaryKey"
#  columns = ["testColumn1", "testColumn2"]
#  DB = boto3.resource("dynamodb")
#  testTable = createTable(DB, tableName, primaryColumnName)
#  assert testTable.table_status == "CREATING"
  # Sleep for 5 seconds to allow time for table to be created
#  time.sleep(7)

# Test deleteTable() function for DynamoDB using deleteTable() function from temperatureHumidity.py

#def test_deleteDynamoTable():
#  DB = boto3.resource("dynamodb")
#  testTable = DB.Table("tableToCreateThenDelete")
#  testTable = deleteTable(testTable)
#  assert testTable.table_status == "DELETING"

# Test insertRow() function for DynamoDB using insertRow() function from temperatureHumidity.py

#def test_insertDynamoRow():
#  DB = boto3.resource("dynamodb")
#  insertionTable = DB.Table("testInsertTable")
#  columns = ["Robot Noise 1", "Robot Noise 2"]
#  primaryColumnName = "Random String Key"
#  attributeOne = "Boop"
#  attributeTwo = "Beep"

  # Method to generate random string used from here: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
#  entryString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

  # Check the number of rows in table before insertion
#  response = insertionTable.scan()
#  tableSizeBefore = len(response["Items"])

#  # Insert new row
#  insertRow(insertionTable, columns, primaryColumnName, entryString, attributeOne, attributeTwo)
#  time.sleep(1)

  # Check the number of rows in table after insertion
#  response = insertionTable.scan()
#  tableSizeAfter = len(response["Items"])

#  assert tableSizeAfter - tableSizeBefore == 1

