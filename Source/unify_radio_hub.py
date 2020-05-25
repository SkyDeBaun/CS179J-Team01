
#unified MQTT library----------------------------------------
import functionalizedAWSIOT
import subscriptionFunctions


#GPIO--------------------------------------------------------
import RPi.GPIO as GPIO

#rfm radio---------------------------------------------------
from RFM69 import Radio, FREQ_915MHZ

#utility-----------------------------------------------------
from datetime import date, datetime
from os import system, name 
import time
import json
import random
import string




#main function-----------------------------------------------
#------------------------------------------------------------
if __name__ == "__main__":
    
    myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()


    while (1):
        print("hello what the f*^*")