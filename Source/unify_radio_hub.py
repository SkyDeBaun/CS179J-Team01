
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

    try:
    
        myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
        print("MQTT Client Initialized")


        #radio tranceiver configuration---------------------------------------------------------
        #---------------------------------------------------------------------------------------
        node_id = 1 #hub node (this)
        network_id = 100 # 1 - 255
        key = "sampleEncryptKey" #must be shared accross all radios on the radio net

        rx_counter = 0.0 #timer counter for checking for incoming data packet
        tx_counter = 0.0 #timer counter 
        up_counter = 0.0 #update counter
        node_counter = 0.0 #when to refresh node counter

        sender = 0 #ID of transmitter
        receiver = 0 #ID of receiver
        data = [] #temp list for grabbing sensor values
        sensorNodes = {} #store discovered active nodes on the radio net into a list
        numberNodes = 0 #save number of nodes on radio transceiver network

        temp = -999.00 #default start values
        lightLevel = -999
        Humidity = -999

        #default state JSON object avoids rare instance of this not being initialized yet (ie if initial data takes longer than 3 seconds )
        JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + str(-999) + '"}}}'

        

        print("Trying to initialize Radio...")
        #initialize radio transceiver------------------------------------------------------------
        #---------------------------------------------------------------------------------------
        radio = Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False)
            #clear()
        print ("INITIALIZING RADIO TRANSCEIVER NETWORK:\n\n")
        time.sleep(0.5)

        while True:

            print ("hello: " + str(rx_counter))

            delay = 0.5 #1/2 second interval
            rx_counter += delay
            tx_counter += delay
            up_counter += delay
            node_counter += delay
            time.sleep(delay)

        
    except KeyboardInterrupt:
        print ("Keyboard exit triggered")

    except Exception as e:
        print(e)


    finally:
        print("Catch all executed")
        #GPIO.cleanup()


