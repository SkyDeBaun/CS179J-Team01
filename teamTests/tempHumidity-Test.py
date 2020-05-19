import os
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT

#Setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Specify the component/pin to be used for temp/humidity sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 20

# Specifiy the pin that will control the DC fan
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)

try:
        while True:
                temperature = None
                humidity = None
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
                if humidity is not None and temperature is not None:

                        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))

                else:
                        print("Failed to retrieve data from humidity sensor")


except KeyboardInterrupt:
        GPIO.cleanup()
