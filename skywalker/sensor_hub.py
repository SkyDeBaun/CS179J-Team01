#skys senseNet hub -> acts as interface between AWS IoT and multiple tranceiver radios(rfm69)
#cs179j -> group 01 -> design project



#imports-----------------------------------------------------
#------------------------------------------------------------

#aws iot-----------------------------------------------------
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
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

 # Callback function triggered when the topic subscribed to gets new published data
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

# Custom Shadow callback------------------------------------- update shadow
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")

    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        #print("------------------------")
        print("\nUPDATING THING SHADOW: " + str(payloadDict["state"]["desired"]["Time"]))

        #print only if not default value----------------------
        myTemp = float(payloadDict["state"]["desired"]["Temperature"])        
        if (myTemp != -999):
            print("Temperature: " + str(myTemp) + " C")
        
        myLight = int(payloadDict["state"]["desired"]["Light"])
        if (myLight != -999):
            print("Light level: " + str(myLight) + "%")


        #print("Update request with token: " + token + " accepted!")
        #print("Temperature: " + str(payloadDict["state"]["desired"]["Temperature"]))
        #print("Light level: " + str(payloadDict["state"]["desired"]["Light"]))
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
        print("GETTING THING SHADOW FROM THE CLOUD: \n")
        print(payloadDict)
        
        #print("Update request with token: " + token + " accepted!")
        #print("Temperature: " + str(payloadDict["state"]["desired"]["Temperature"]))
        #print("Light level: " + str(payloadDict["state"]["desired"]["Light"]))
        #print("Time Stamp: " + str(payloadDict["state"]["desired"]["Time"]))
        print("\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- delete shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        #print("------------------------")
        #print("Delete request with token: " + token + " accepted!")
        #print("DELETING THING SHADOW FROM THE CLOUD")
        print("Refreshing Node Buffer")
        print("\n")
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
root_CA = "../Certificates/root-CA.crt"
private_key = "../Certificates/device-private.pem.key"
certificate = "../Certificates/device-certificate.pem.crt"
client_ID = generateClient_ID()
thing_name = "Pi_sense01"



#MQTT subscription/publication-----------------------------------------------

Device_ID = "Pi_sense01"

# AWS IoT certificate based connection---------------------------------------
myMQTTClient = AWSIoTMQTTClient(Device_ID)#this can be any arbitrary string
myMQTTClient.configureEndpoint(AWS_IoT_endpoint, port)#endpoint and port number
myMQTTClient.configureCredentials(root_CA, private_key, certificate)#root ca and certificate used for secure connection

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish----------------------------------------------------------
myMQTTClient.connect()
#myMQTTClient.subscribe("Pi_sense01/data", 1, myCallBack)





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
#deviceShadowHandler.shadowGet(customShadowCallback_Get, 5)
#deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) #delete first to clear existing doc (in case additions to Shadow doc)



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

#default state JSON object avoids rare instance of this not being initialized yet (ie if initial data takes longer than 3 seconds )
JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + str(-999) + '"}}}'


#initialize radio tranceiver------------------------------------------------------------
#---------------------------------------------------------------------------------------
with Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False) as radio:
    clear()
    print ("INITIALIZING RADIO TRANSCEIVER NETWORK:\n\n")
    time.sleep(0.5)

    while True:
        
        # Every 1 seconds check for packets----------------------------------
        if rx_counter >= 1:
            rx_counter = 0.0 #reset counter
            
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
                        temp = float(parse[1])
                        #print("WFT: " + str(temp))
                        temp = (temp/100.0) #convert to float (puts in decimal form)
                        #print("WFT: " + str(temp))

                    elif sensorType == "Light":
                        lightLevel = parse[1].replace("%", "")
                        lightLevel = int(lightLevel)
                    
                    sensorNodes[str(sender)] = sensorType #add new node -> overwrites previous values if key pair exists already

                    
                    #collate recieved sensor data------------------------------- 
                    now = datetime.utcnow()#iso timestamp
                    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
                    JSONPayload = '{"state":{"desired":{"Light":' + str(lightLevel) + ', "Temperature":  ' + str(temp) +', "Time": "' + now_str + '"}}}'

            #else no packets

            
                    
        #3 second counter-------------------------------------------------------
        if up_counter > 2.0: #every 2 seconds
            up_counter = 0

            #clear() #refresh screen

            #list nodes in dictionary
            print("--------------------------------------------------------------")
            print("TRANSCEIVER NODES ON THE NETWORK: " + str(len(sensorNodes)))
            for key in sensorNodes:
                print("Node " + key + ": " + str(sensorNodes[key]))                        

            #update shadow -----------------------------------------------------
            if len(sensorNodes) > 0: #only send if 1 or more nodes
                deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5) #5 is token setting (?)

            #get subcription


            myMQTTClient.subscribe("Pi_sense01/data", 1, myCallBack)
            myMQTTClient.subscribe("ryan_pi/data", 1, myCallBack)




        #reset dict on nodes----------------------------------------------------
        if node_counter > 10.0: # every 21 seconds
            node_counter = 0.0

            #reset dict and shadow
            sensorNodes.clear() #clear dict of active nodes -> refresh the dictionary  
            deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)#delete shadow...
            temp = -999.00 #default start values
            lightLevel = -999
  

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
        delay = 0.5 #1/2 second interval
        rx_counter += delay
        tx_counter += delay
        up_counter += delay
        node_counter += delay

        time.sleep(delay)