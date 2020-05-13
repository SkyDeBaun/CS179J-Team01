import RPi.GPIO as GPIO
import os
import sys
import boto3
import Adafruit_DHT
from time import sleep
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal


while True:

    tableName = "tempHumidityData"
    primaryColumnName = "entryNumber"

    # resource
    DB = boto3.resource("dynamodb")
    table = DB.Table(tableName)

    response = table.scan(
        FilterExpression=Attr(primaryColumnName).gte(0)
    )

    totalValues = 0
    humiditySum = 0
    temperatureSum = 0

    for row in response["Items"]:
        humiditySum += row["humidity"]
        temperatureSum += row["temperature"]
        totalValues += 1

    humidityAvg = humiditySum / totalValues
    temperatureAvg = temperatureSum / totalValues
    humidityAvg = round(humidityAvg, 2)
    temperatureAvg = round(temperatureAvg, 2)


    print(f"Humidity average is: {humidityAvg}")
    print(f"Temperature average is: {temperatureAvg}")
    print("####")

    sleep(5)

