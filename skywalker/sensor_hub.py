#skys senseNet hub -> acts as interface between AWS IoT and multiple tranceiver radios(rfm69)
#cs179j -> group 01 -> design project



#imports-----------------------------------------------------
#------------------------------------------------------------

#aws iot-----------------------------------------------------
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

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



#function definitions-------------------------------------------------------------------
#---------------------------------------------------------------------------------------

# Custom Shadow callback------------------------------------- update shadow
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        #print("------------------------")
        print("\nUPDATING THING SHADOW: ")
        
        #print("Update request with token: " + token + " accepted!")
        print("Temperature: " + str(payloadDict["state"]["desired"]["Temperature"]))
        print("Light level: " + str(payloadDict["state"]["desired"]["Light"]))
        #print("Time Stamp: " + str(payloadDict["state"]["desired"]["Time"]))
        print("\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- get shadow
def customShadowCallback_Get(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        #print("------------------------")
        print("GETTING THING SHADOW FROM THE CLOUD: ")
        print(payloadDict)
        
        #print("Update request with token: " + token + " accepted!")
        #print("Temperature: " + str(payloadDict["state"]["desired"]["Temperature"]))
        #print("Light level: " + str(payloadDict["state"]["desired"]["Light"]))
        #print("Time Stamp: " + str(payloadDict["state"]["desired"]["Time"]))
        print("\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- delete shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        #print("------------------------")
        #print("Delete request with token: " + token + " accepted!")
        print("DELETING THING SHADOW FROM THE CLOUD")
        print("\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- shadow Delta (for subscription)
def customShadowCallback_Delta(payload, responseStatus, token):
# payload is a JSON string ready to be parsed using json.loads(...)
        print("Received a message: ")
        payloadDict = json.loads(payload)
        LEDval = payloadDict["state"]["Temperature"] #get value from JSON field
        print ("Requested Temperature Value: " + str(LEDval))
        print ("Requested Time Stamp: " + payloadDict["state"]["Time"])
        print ("Token: " + str(token)) 
        print (" ")        
        #deltaMessage = json.dumps(payloadDict["state"])
        #print(deltaMessage)


# Generate random Client_ID----------------------------------- generate random ID
def generateClient_ID(stringLength = 10):
    client_string = string.ascii_letters + string.digits
    return ''.join((random.choice(client_string) for i in range(stringLength)))

# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 




        

#AWS IoT MQTT configuration-------------------------------------------------------------
#---------------------------------------------------------------------------------------

#client config----------------------------------------------- CLIENT SETTINGS
AWS_IoT_endpoint = "a3te7fgu4kv468-ats.iot.us-west-1.amazonaws.com"
port = 8883
root_CA = "cert/rootCA.pem.crt"
private_key = "cert/333052c1bf-private.pem.key"
certificate = "cert/333052c1bf-certificate.pem.crt"
client_ID = generateClient_ID()
thing_name = "Pi_sense01"


# Init AWSIoTMQTTShadowClient--------------------------------
myAWSIoTMQTTShadowClient = None

#configure shadow--------------------------------------------
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(client_ID) #this can be any arbitrary string
myAWSIoTMQTTShadowClient.configureEndpoint(AWS_IoT_endpoint, port) #endpoint and port number
myAWSIoTMQTTShadowClient.configureCredentials(root_CA, private_key, certificate )#root ca and certificate used for secure connection

# AWSIoTMQTTShadowClient configuration-----------------------
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT-----------------------------------------
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription---------
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thing_name, True)

#get the last shadow (1 time only) - if exists (callback prints message on failure to retrieve-> ie if no shadow exists)
deviceShadowHandler.shadowGet(customShadowCallback_Get, 5)
deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) #delete first to clear existing doc (in case additions to Shadow doc)



#radio tranceiver configuration---------------------------------------------------------
#---------------------------------------------------------------------------------------
node_id = 1 #hub node (this)
network_id = 100 # 1 - 255
key = "sampleEncryptKey" #must be shared accross all radios on the radio net

rx_counter = 0.0 #timer counter for checking for incoming data packet
tx_counter = 0.0 #timer counter 
up_counter = 0.0 #update counter

sender = 0 #ID of transmitter
receiver = 0 #ID of receiver
data = [] #temp list for grabbing sensor values
sensorNodes = {} #store discovered active nodes on the radio net into a list
numberNodes = 0 #save number of nodes on radio transceiver network

temp = -999.99 #default start values
lightLevel = -99

#default state JSON object avoids rare instance of this not being initialized yet (ie if initial data takes longer than 3 seconds )
JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + str(-999) + '"}}}'


#initialize radio tranceiver------------------------------------------------------------
#---------------------------------------------------------------------------------------
with Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False) as radio:
    print ("\nINITIALIZING TRANSCEIVER RADIO...\n\n")
        
    while True:
        
        # Every 2 seconds check for packets----------------------------------
        if rx_counter > 1:
            rx_counter = 0 #reset counter
            
            if radio.has_received_packet():
                #print("\n\nData Packet Received")
                
                # Process packets
                for packet in radio.get_packets():
                    sender = packet.sender
                    receiver = packet.receiver
                    data = packet.data
                    
                    datastring = ""
                    for x in data:
                        datastring += chr(x) #convert to char and add to string
                    
                    #output received data--------------------------------------
                    '''
                    print("---------------------------------")
                    print("Receiver Node: \t" + str(receiver))
                    print("Sender Node: \t" + str(sender))
                    print("Data String: \t" + str(datastring))
                    print("\n")
                    '''

                    #parse radio data string for value pair--------------------
                    parse = datastring.split(" ")
                    #print("Parse-------------------------------results:")
                    #print("Parse 0: " + str(parse[0]))
                    #print("Parse 1: " + str(parse[1]))

                    sensorType = str(parse[0].replace(":","")) #clean junk from parsed string

                    if sensorType == "Temperature":
                        temp = int(parse[1])
                        temp = temp/100 #convert to float (puts in decimal form)

                    elif sensorType == "Light":
                        lightLevel = parse[1].replace("%", "")
                        lightLevel = int(lightLevel)
                    
                    #store dictionary of nodes on radio network
                    if str(sender) not in sensorNodes:                        
                        sensorNodes[str(sender)] = sensorType #add new node

                    numberNodes = len(sensorNodes) #count the nodes

                    
                    #collate recieved sensor data------------------------------- 
                    now = datetime.utcnow()#iso timestamp
                    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
                    JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + now_str + '"}}}'
                    
                    
        #3 second counter-------------------------------------------------------
        if up_counter > 3: #every 3 seconds
            up_counter = 0

            #list nodes in dictionary


            print("TRANSCEIVER NODES ON THIS NETWORK: " + str(numberNodes))
            for val in sensorNodes:
                print("Node " + val + ": " + sensorNodes[val])            
            
            
            sensorNodes.clear() #clear dict of active nodes -> refresh the dictionary    


            #update shadow -----------------------------------------------------
            if numberNodes > 0: #only send if 1 or more nodes
                deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5) #5 is token setting (?)


        #5 second counter-------------------------------------------------------
        if tx_counter > 5: # every 5 seconds
            tx_counter = 0.0

                               

            #test send message------------------------------------------------------ Future use: probing for devices on the network
            #-----------------------------------------------------------------------> or remote control
            '''
            print ("Sending to node: " + str(recipient_id))
            if radio.send(recipient_id, "TEST: " + str(counter), attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")
            '''

        #print("Listening...", len(radio.packets), radio.mode_name)
        delay = .5 #1/2 second interval
        rx_counter += delay
        tx_counter += delay
        up_counter += delay

        #print("RX Counter: " + str(rx_counter))
        time.sleep(delay)