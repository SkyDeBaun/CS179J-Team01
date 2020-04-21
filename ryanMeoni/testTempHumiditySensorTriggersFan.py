from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import sys
from datetime import date, datetime
import RPi.GPIO as GPIO
import Adafruit_DHT

# Setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Specify the component/pin to be used for temp/humidity sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 20

# Specifiy the pin that will control the DC fan
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint(
    "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/AWS_certs/Amazon_Root_CA_1.pem",
                                  "/home/pi/AWS_certs/1aac3835be-private.pem.key", "/home/pi/AWS_certs/1aac3835be-certificate.pem.crt")
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()
try:
    while True:
        temperature = None
        humidity = None
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:

            print(
                "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))

            #  Turn fan on (set output low) if humidity greater than 90% (would use temperature in practice, but hard to vary temperature on demand for testing purposes)
            if humidity > 90:
                GPIO.output(16, GPIO.LOW)
                now = datetime.utcnow()
                now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                payload = '{ "timestamp": "' + now_str + '","temperature": ' + \
                    str(temperature) + ',"humidity": ' + str(humidity) + ' }'
                print(payload)
                myMQTTClient.publish("ryanpi/data", payload, 0)

            else:
                GPIO.output(16, GPIO.HIGH)

        else:
            print("Failed to retrieve data from humidity sensor")
        sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
