#skywalker intefaces rfm69 900 MHz radio transceivers with Raspberry Pi
#using pypi.org wrapper for LowPowerLabs rfm69 library
#https://pypi.org/project/rpi-rfm69/



from RFM69 import Radio, FREQ_915MHZ
import datetime
import time
import json

node_id = 1
network_id = 100
recipient_id = 77
key = "sampleEncryptKey"

with Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False) as radio:
    print ("Radio initialized..")
    
    rx_counter = 0
    tx_counter = 0
    temperature = 0
    counter = 0
    
    sender = 0 #ID of transmitter
    receiver = 0 #ID of receiver
    data = []
    while True:
        
        # Every 1 seconds check for packets----------------------------------
        if rx_counter > 1:
            rx_counter = 0 
            
            if radio.has_received_packet():
                print("\n\nPacket received!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
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
        
        #test send message------------------------------------------------------ Future use: probing for devices on the network
        # Every 5 seconds send a test message
        if tx_counter > 5:
            tx_counter=0
            
            #temperature = radio.read_temperature()
            #print("Internal Temperature: " + str(temperature) + "C")
            
            # Send
            print ("Sending to node: " + str(recipient_id))
            if radio.send(recipient_id, "TEST: " + str(counter), attempts=3, waitTime=100):
                print ("Acknowledgement received")
            else:
                print ("No Acknowledgement")
            

        print("Listening...", len(radio.packets), radio.mode_name)
        delay = 1
        rx_counter += delay
        tx_counter += delay
        
        time.sleep(delay)