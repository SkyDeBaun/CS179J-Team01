
# unified MQTT library----------------------------------------
import functionalizedAWSIOT
import functionalizedRadio
import subscriptionFunctions

# utility-----------------------------------------------------
from datetime import date, datetime
from os import system, name
import time
import json
import random
import string

#my radio network specific variables--------------------------
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

# default state JSON object avoids rare instance of this not being initialized yet (ie if initial data takes longer than 3 seconds )
JSONPayload = '{"Light":' + str(
    lightLevel) + ', "Temperature":  ' + str(temp) + ', "Time": "' + str(-999) + '"}'


#functions-------------------------------------------------------
#----------------------------------------------------------------

# clear screen function------------------------------------------
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


# main function-----------------------------------------------
# ------------------------------------------------------------
if __name__ == "__main__":

    try:
        # initialize AWS MQTT----------------------------------
        myMQTTClient = functionalizedAWSIOT.AWS_MQTT_Initialize()
        print("MQTT Client Initialized")

        # initialize radio transceiver------------------------------------------------------------
        # ---------------------------------------------------------------------------------------
        radio = functionalizedRadio.initializeRadio()
        radio.send(1, "0", attempts=1, waitTime=100) #hack to overcome new issue - radios dead until radio.send!

        #subscriptionFunctions.interfaceRadio(radio) #hack to provide radio object to subscription functions
        clear()
        print("RADIO NETWORK INITIALIZED:\n\n")


        while True:
            # Every 1 seconds check for packets----------------------------------
            if rx_counter >= 1:
                rx_counter = 0.0  # reset counter

                if radio.has_received_packet():
                    # print("\n\nData Packet Received")

                    # Process packets
                    for packet in radio.get_packets():
                        sender = packet.sender
                        receiver = packet.receiver
                        data = packet.data

                        datastring = "" #reset data string
                        for x in data:
                            # convert to char and add to string
                            datastring += chr(x)

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
                        # clean junk from parsed string
                        sensorType = str(parse[0].replace(":", ""))

                        # my radio node specific sensorTypes-------------------------
                        if sensorType == "Temperature":
                            temp = float(parse[1])
                            # convert to float (puts in decimal form)
                            temp = (temp/100.0)

                        elif sensorType == "Light":
                            lightLevel = parse[1].replace("%", "")
                            lightLevel = int(lightLevel)

                        # add new node -> overwrites previous values if key pair exists already
                        sensorNodes[str(sender)] = sensorType

                        # collate recieved sensor data-------------------------------
                        now = datetime.utcnow()  # iso timestamp
                        # e.g. 2016-04-18T06:12:25.877Z
                        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                        JSONPayload = '{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(
                            temp) + ', "Time": "' + now_str + '"}'

                # else no packets recieved

            # 3 second counter-------------------------------------------------------
            if up_counter > 2.0:  # every 2 seconds
                up_counter = 0

                # list active nodes on network----------------------------------------
                print("--------------------------------------------------------------")
                print("TRANSCEIVER NODES ON THE NETWORK: " +
                      str(len(sensorNodes)))
                for key in sensorNodes:
                    print("Node " + key + ": " + str(sensorNodes[key]))

                # publish to my Thing-------------------------------------------------
                if len(sensorNodes) > 0:  # only send if 1 or more nodes
                    myMQTTClient.publish("Pi_sense01/data", JSONPayload, 0)

                # get subcriptions----------------------------------------------------
                myMQTTClient.subscribe("Pi_sense01/data", 1, subscriptionFunctions.subRadioNodes) #verifies my ealier publish + prints to console
                myMQTTClient.subscribe("ryan_pi/data", 1, subscriptionFunctions.subHumiture)
                myMQTTClient.subscribe("ReynaPi/ultrasonic", 1, subscriptionFunctions.subUltrasonic)
                                

            # reset dictionary of nodes--------------------------------------------------
            if node_counter > 10.0:  # every 10 seconds
                node_counter = 0.0

                # reset dict and shadow
                sensorNodes.clear()  # clear dict of active nodes -> refresh the dictionary
                temp = -999.00  #reset to default start values
                lightLevel = -999

            delay = 0.5  # 1/2 second interval
            rx_counter += delay
            tx_counter += delay
            up_counter += delay
            node_counter += delay
            time.sleep(delay)


    except KeyboardInterrupt:
        print("Keyboard Exit")

    except Exception as e:
        print("An Error Occured:")
        print(e)  # print exception messages

    finally:
        print("Terminating Program: Radio Network Offline")
