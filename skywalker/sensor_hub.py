#skys senseNet hub -> acts as interface between AWS IoT and tranceiver radios
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
import time
import json
import random
import string



#function definitions-------------------------------------------------------------------
#---------------------------------------------------------------------------------------

# Custom Shadow callback------------------------------------- update shadow
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("Temperature value: " + str(payloadDict["state"]["desired"]["Temperature"]))
        print("Time Stamp: " + str(payloadDict["state"]["desired"]["Time"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- delete shadow
def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!") #no shadow to get!


# Custom Shadow callback------------------------------------- shadow Delta
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

#get last shadow (1 time only) - if exists (callback prints message on failure to retrieve)
deviceShadowHandler.shadowGet(customShadowCallback_Update, 5)

deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) #delete first to clear existing doc


#update shadow on Delta (change) only-------------------------
deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)



#radio tranceiver configuration---------------------------------------------------------
#---------------------------------------------------------------------------------------
node_id = 1 #hub node
network_id = 100 # 1 - 255
key = "sampleEncryptKey" #must be shared accross all radios on the radio net

rx_counter = 0 #timer counter for checking for incoming data packet
tx_counter = 0 #timer counter 
temperature = 0 #radio's internal temperture    
sender = 0 #ID of transmitter
receiver = 0 #ID of receiver
data = [] 
nodes = [] #save discovered active nodes on the radio net


#initialize radio tranceiver------------------------------------------------------------
#---------------------------------------------------------------------------------------
with Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False) as radio:
    print ("Radio initialized..")
        
    while True:
        
        # Every 2 seconds check for packets----------------------------------
        if rx_counter > 1:
            rx_counter = 0 

            
            if radio.has_received_packet():
                print("\n\nData Packet Received")
                
                # Process packets
                for packet in radio.get_packets():
                    #print (packet)
                    sender = packet.sender
                    receiver = packet.receiver
                    data = packet.data
                    datastring = ""
                    for x in data:
                        datastring += chr(x) #convert to char and add to string
                    
                    #output received data--------------------------------------
                    print("---------------------------------")
                    print("Receiver Node: \t" + str(receiver))
                    print("Sender Node: \t" + str(sender))
                    print("Data String: \t" + str(datastring))
                    print("\n")

                    parse = datastring.split(" ")
                    sensorType = str(parse[0])
                    sensorValue = int(parse[1])
                    sensorValue = sensorValue/100

                    print("Parse-------------------------------results:")
                    print("Parse 0: " + str(sensorType))
                    print("Parse 1: " + str(sensorValue))


                    #send recieved sensor data to cloud------------------------- TEST
                    now = datetime.utcnow()#iso timestamp
                    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
                    #JSONPayload = '{"state":{"desired":{"property":' + str(rx_counter) + ', "LED": '+ str(datastring) + ', "Time": "' + now_str + '"}}}'
                    JSONPayload = '{"state":{"desired":{"property":' + str(7) + ', "Temperature": "' + str(sensorValue) + '", "Time": "' + now_str + '"}}}'

                    deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5) #5 is token setting (?)

        
        #test send message------------------------------------------------------ Future use: probing for devices on the network
        # Every 5 seconds send a test message
        if tx_counter > 5:
            tx_counter=0

            #test
            deviceShadowHandler.shadowGet(customShadowCallback_Update, 5)
            #deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)


            
            #temperature = radio.read_temperature()
            #print("Internal Temperature: " + str(temperature) + "C")
            
            # Send
            '''
            print ("Sending to node: " + str(recipient_id))
            if radio.send(recipient_id, "TEST: " + str(counter), attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")
            '''

        #print("Listening...", len(radio.packets), radio.mode_name)
        delay = .5
        rx_counter += delay
        tx_counter += delay
        

        #print("RX Counter: " + str(rx_counter))
        time.sleep(delay)