
# unified MQTT library----------------------------------------
import functionalizedAWSIOT
import subscriptionFunctions


# GPIO--------------------------------------------------------
import RPi.GPIO as GPIO

# rfm radio---------------------------------------------------
from RFM69 import Radio, FREQ_915MHZ

# utility-----------------------------------------------------
from datetime import date, datetime
from os import system, name
import time
import json
import random
import string



#callbacks-----------------------------------------------------
# Callback function triggered when the topic subscribed to gets new published data
def myCallBack(self, params, packet):
        #print(packet.payload)
        
        payloadDict = json.loads(packet.payload)
        global Temp
        global Humidity
        
        Temp = payloadDict ["temperature"] #get value from JSON field        
        Humidity = payloadDict["humidity"] #get value

        print("Ryan's Sensor Data---------------------- ")
        print("Temperature: " + str(Temp))
        print("Humidity: " + str(Humidity))
        print(" ")

        if float(Humidity) > 85.0:
            print ("HIGH HUMIDITY THRESHOLD*****************\n")        

        print("")













# main function-----------------------------------------------
# ------------------------------------------------------------
if __name__ == "__main__":

    try:

        myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
        print("MQTT Client Initialized")

        # radio tranceiver configuration---------------------------------------------------------
        # ---------------------------------------------------------------------------------------
        node_id = 1  # hub node (this)
        network_id = 100  # 1 - 255
        key = "sampleEncryptKey"  # must be shared accross all radios on the radio net

        rx_counter = 0.0  # timer counter for checking for incoming data packet
        tx_counter = 0.0  # timer counter
        up_counter = 0.0  # update counter
        node_counter = 0.0  # when to refresh node counter

        sender = 0  # ID of transmitter
        receiver = 0  # ID of receiver
        data = []  # temp list for grabbing sensor values
        sensorNodes = {}  # store discovered active nodes on the radio net into a list
        numberNodes = 0  # save number of nodes on radio transceiver network

        temp = -999.00  # default start values
        lightLevel = -999
        Humidity = -999

        # default state JSON object avoids rare instance of this not being initialized yet (ie if initial data takes longer than 3 seconds )
        JSONPayload = '{"state":{"desired":{"Light":' + str(
            lightLevel) + ', "Temperature":  ' + str(temp) + ', "Time": "' + str(-999) + '"}}}'

        print("INITIALIZING RADIO TRANSCEIVER NETWORK:\n\n")
        # initialize radio transceiver------------------------------------------------------------
        # ---------------------------------------------------------------------------------------
        radio = Radio(FREQ_915MHZ, node_id, network_id,
                      encryptionKey=key, isHighPower=True, verbose=False)
        # clear()
        print("RADIO INITIALIZED:\n\n")
        time.sleep(0.5)

        while True:
            
            # Every 1 seconds check for packets----------------------------------
            if rx_counter >= 1:
                rx_counter = 0.0 #reset counter
                
                if radio.has_received_packet():
                    # print("\n\nData Packet Received")
                    
                    # Process packets
                    for packet in radio.get_packets():
                        sender = packet.sender
                        receiver = packet.receiver
                        data = packet.data
                        
                        datastring = ""
                        for x in data:
                            datastring += chr(x) #convert to char and add to string
                        
                        # output received data--------------------------------------
                        '''
                        print("---------------------------------")
                        print("Receiver Node: \t" + str(receiver))
                        print("Sender Node: \t" + str(sender))
                        print("Data String: \t" + str(datastring))
                        print("\n")
                        '''

                        # parse radio data string for value pair--------------------
                        parse = datastring.split(" ")
                        # print("Parse-------------------------------results:")
                        # print("Parse 0: " + str(parse[0]))
                        # print("Parse 1: " + str(parse[1]))

                        sensorType = str(parse[0].replace(":","")) #clean junk from parsed string

                        if sensorType == "Temperature":
                            temp = float(parse[1])
                            temp = (temp/100.0) #convert to float (puts in decimal form)

                        elif sensorType == "Light":
                            lightLevel = parse[1].replace("%", "")
                            lightLevel = int(lightLevel)
                        
                        sensorNodes[str(sender)] = sensorType #add new node -> overwrites previous values if key pair exists already

                        
                        # collate recieved sensor data------------------------------- 
                        now = datetime.utcnow()#iso timestamp
                        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
                        JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + now_str + '"}}}'

                # else no packets

                
                        
            # 3 second counter-------------------------------------------------------
            if up_counter > 2.0: #every 2 seconds
                up_counter = 0

                # list nodes in dictionary
                print("--------------------------------------------------------------")
                print("TRANSCEIVER NODES ON THE NETWORK: " + str(len(sensorNodes)))
                for key in sensorNodes:
                    print("Node " + key + ": " + str(sensorNodes[key]))                        

                # update shadow -----------------------------------------------------
                if len(sensorNodes) > 0: #only send if 1 or more nodes
                    #deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5) #5 is token setting (?)
                    print("hello shadow")

                # get subcription----------------------------------------------------
                myMQTTClient.subscribe("Pi_sense01/data", 1, subscriptionFunctions.hello)
                myMQTTClient.subscribe("ryan_pi/data", 1, subscriptionFunctions.subHumiture)
                # print("Humidity: " + str(float(Humidity)))

                if float(Humidity) > 80:
                    if radio.send(21, "1", attempts=2, waitTime=100):
                        # print ("LED Control Message -> On")
                        print("") #stupid -> python complains if above print line commented (inside if statement)
                    else:
                        # print ("LED Control Message -> No Acknowledgement")
                        print("")
                else:
                    if radio.send(21, "0", attempts=2, waitTime=100):
                        # print ("LED Control Message -> Off")
                        print("")

                


            # reset dict on nodes----------------------------------------------------
            if node_counter > 10.0: # every 21 seconds
                node_counter = 0.0

                # reset dict and shadow
                sensorNodes.clear() #clear dict of active nodes -> refresh the dictionary  
                #deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)#delete shadow...
                temp = -999.00 #default start values
                lightLevel = -999
    

                # test send message------------------------------------------------------ Future use: probing for devices on the network
                # -----------------------------------------------------------------------> or remote control
                '''
                print ("Sending to node: " + str(recipient_id))
                if radio.send(recipient_id, "TEST: " + str(counter), attempts=3, waitTime=100):
                    print ("Acknowledgement received")
                else:
                    print ("No Acknowledgement")
                '''
            

            # print("Listening...", len(radio.packets), radio.mode_name)
            delay = 0.5 #1/2 second interval
            rx_counter += delay
            tx_counter += delay
            up_counter += delay
            node_counter += delay

            time.sleep(delay)

        
    except KeyboardInterrupt:
        print ("Keyboard exit triggered")

    except Exception as e:
        print(e) #print any other exception messages


    finally:
        print("Terminating Program: Radio Network Offline")


