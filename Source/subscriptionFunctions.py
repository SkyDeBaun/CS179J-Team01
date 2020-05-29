import cameraCode
import reynaPiNode
import helpers
import RPi.GPIO as GPIO
import functionalizedRadio
import json
from decimal import Decimal


# Should be in form customCallback(client, userdata, message)
# where message contains topic and payload.
# Note that client and userdata are here just to be aligned with the underneath Paho callback function signature.
# These fields are pending to be deprecated and should not be depended on.

def picture(client, userdata, message):
    bucketName = "senior-design-camera-files"
    try:
        fileName = cameraCode.takePicture()
        helpers.uploadToS3(fileName[0], bucketName,
                           helpers.getAWSCredentials())
    finally:
        print("Taking picture and uploading to S3 bin")
        return True


def controlFan(self, params, packet):
    payloadDict = json.loads(packet.payload)
    humidity = Decimal(payloadDict["humidity"])
    print(packet.payload)
    if (humidity > 85):
        print("Fan is ON")
        print("####")
        GPIO.output(16, GPIO.LOW)
        return 1

    else:
        print("Fan is OFF")
        print("####")
        GPIO.output(16, GPIO.HIGH)
        return 0


def ultrasonic(client, userdate, message):
    distance = 0
    payloadInfo = json.loads(message.payload)
    distance = payloadInfo["distance"]
    if distance < 15:
        reynaPiNode.stop1()
        return 0
    else:
        reynaPiNode.go1()
        return 1


def motor2(client, userdate, message):
    humidity = 0
    payloadInfo = json.loads(message.payload)
    humidity = payloadInfo["humidity"]
    print("humidity:", str(humidity))
    humidity = int(humidity)
    if humidity < 65:
        reynaPiNode.stop2()
        return 0
    else:
        reynaPiNode.go2()
        return 1


# subscribe to Ryan's humidity/temperature sensor-----
def subHumiture(client, userdate, message):
    payloadInfo = json.loads(message.payload)   
    humidity = payloadInfo["humidity"]
    temperature = payloadInfo["temperature"]

    print("\nRyan's Humiture Data:")
    print("Temperature: ", str(temperature), "\tHumidity:", str(humidity))
    if float(humidity) > 85.0:  # print warning if threshold reached
        print("HIGH HUMIDITY THRESHOLD REACHED!\n")

    if float(humidity) > 80:
        if radio.send(21, "1", attempts=2, waitTime=100):
            print ("LED Control Message -> On")        
    else:
        if radio.send(21, "0", attempts=2, waitTime=100):
            #print ("LED Control Message -> Off")
            print("")


# subscribe to Sky's radio network data------------------
def subRadioNodes(client, userdate, message):
    payloadInfo = json.loads(message.payload)
    myTemp = float(payloadInfo["Temperature"])
    myLight = int(payloadInfo["Light"])
    print("\nRadio Network Data: ")

    #print values from active nodes only
    if (myTemp != -999):  # print only if not default value
        print("Temperature: " + str(myTemp) + " C")

    if (myLight != -999):
        print("Light level: " + str(myLight) + "%")

    print("\n")

# subscribe to Reyna's ultrasonic sensor data-------------
def subUltrasonic(client, userdate, message):
    payloadInfo = json.loads(message.payload)
    distance = payloadInfo["distance"]
    print("Reyna's Sensor Data: ")
    print("Distance: ", int(distance))
    print("\n")

#radio specific only--------------------------------------
def interfaceRadio():
    global radio #refers to variable in functionalizedRadio
    radio = functionalizedRadio.initializeRadio()
    return radio


subscribedTopicDictionary = {
    "picture": picture,
    "controlFan": controlFan,
    "ultrasonic": ultrasonic,
    "motor2": motor2,
    "subHumiture": subHumiture,
    "subRadioNodes": subRadioNodes,
    "subUltrasonic": subUltrasonic

    # FIXME Find some way to not hardcode value names
}


# https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute
# Maybe check if k is valid input
def generateCallbackFunction(k):
    return subscribedTopicDictionary[k]
