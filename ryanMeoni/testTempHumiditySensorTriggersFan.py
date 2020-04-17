import RPi.GPIO as GPIO
import Adafruit_DHT

#Setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Specify the component/pin to be used for temp/humidity sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 20

# Specifiy the pin that will control the DC fan
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(16, GPIO.HIGH)

while True:
        temperature = None
        humidity = None

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:

                print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))

                #  Turn fan on if humidity greater than 90% (would use temperature in practice, but hard to vary temperature on demand for testing purposes)
                if humidity > 90:
                        GPIO.output(16, GPIO.HIGH)
                else:
                        GPIO.output(16, GPIO.LOW)

        else:
                print("Failed to retrieve data from humidity sensor")
