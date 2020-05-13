import RPi.GPIO as GPIO
import os
import sys
import boto3
import Adafruit_DHT
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import functionalizedAWSIOT
from datetime import date, datetime

def insertRow(table, columns, primaryColumnName, entryNumber, temperature, humidity):
    # test that we can insert a new row into table with a given primary key (entryNumber)

    response = table.put_item(
        Item={
            primaryColumnName: entryNumber,
            columns[0]: temperature,
            columns[1]: humidity
        }
    )


def printAllRows(table, primaryColumnName):
    # print all table entries to test we inserted rows correctly
    # get all rows with a primary key (entryNumber) greater than or equal to 0 (so all of them)

    response = table.scan(
        FilterExpression=Attr(primaryColumnName).gte(0)
    )

    for row in response["Items"]:
        print(row)

def createTable(DB, tableName, primaryColumnName, columns):

    table = DB.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': primaryColumnName,
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primaryColumnName,
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == "__main__":

    #Initialize MQTT client
    myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()

    # GPIO set up
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Specify the component/pin to be used for temp/humidity sensor
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 20


    # entryNumber is my primary key!
    # setup fields
    tableName = "tempHumidityData"
    primaryColumnName = "entryNumber"
    columns = ["temperature", "humidity"]

    # resource
    DB = boto3.resource("dynamodb")
    oldTable = DB.Table(tableName)

    # Delete existing table
    oldTable.delete()

    sleep(3)
    print("OLD TABLE DELETED")

    # Create new table
    newTable = createTable(DB, tableName, primaryColumnName, columns)

    sleep(5)
    print("NEW TABLE CREATED")

    # test insert row with entryNumber of 1
    entryNumber = 1
    while True:
        temperature = None
        humidity = None
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:

            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            temperature = Decimal(temperature)
            temperature = round(temperature, 2)
            humidity = Decimal(humidity)
            humidity = round(humidity, 2)
            insertRow(newTable, columns, primaryColumnName, entryNumber, temperature, humidity)
            now = datetime.utcnow()
            now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' }'
            myMQTTClient.publish("ryan_pi/data", payload, 0)

        else:
            print("Failed to retrieve data from humidity sensor")

        entryNumber = entryNumber + 1
        #if (entryNumber == 10):
        #    break

        sleep(2)

    # print all our rows
    printAllRows(newTable, primaryColumnName)
