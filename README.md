# CS179J - Senior Design Project

# Extensible Sensor Network

## Project Description

### System Overview
This project provides remote environmental and security monitoring and actuator control using inexpensive off the shelf components (Raspberry Pi's).

### System Purpose
The Extensible Sensor Network (ESN) is an Internet of Things (IoT) framework for monitoring and control of remote sensors, actuators, and security devices using the Amazon Web Services (AWS) IoT framework.

### System Context
The system’s extensible sub-networks of remote sensors, actuators, and security devices communicate with AWS IoT cloud servers functioning as the central hub (Device Gateway) of the system. This Device Gateway provides a means of capitalizing on AWS Security, Lambdas, and Message Broker protocols for inter-device communication and rules based control across the network. Additionally, the Device Gateway facilitates transmission of alerts via SMS messages and provides the means of implementing a unified system interface for the real-time monitoring and control of the network’s sensors and devices.


## AWS Setup
This project utilizes Amazon Web Services IoT Core to securely connect to and facilitate communications between devices and the cloud using the MQTT messaging protocol.

1. Create an AWS account
1. Create IAM user accounts to manage access controls (if needed)
1. Select Region providing desired services (Oregon offers the most features)
1. Create and configure device Things (includes x.509 secure certificates)
1. Download secure certificates for project “Certificates” directory
1. Create and configure AWS Rules and/or Lambdas (as needed)



## Python Dependencies
Project has only been tested for Python 3.6+
We recommend that you set up a python virtual environment before continuing

## Project Installation
- Use a `git clone` or download this repository
- Activate your Python virtualenv
- Navigate to the base directory of this repository on your device
- Run `pip install -r requirements.txt`

## Hardware Setup
All subsystems use Raspberry Pi’s for WiFi connectivity and GPIO functionality.

### Sensor Module
BCM pin numbers 16, 20, and 21. 16 for sending on/off signal to relay that powers DC fan. 20 for input pin from DHT 22 temperature/humidity sensor. 21 for signal from tripwire laser reciever. 

<p align="center">
  <img src="/Images/raspberry-pi-pinout_ryan.png">
</p>


### Radio Module:
The radio subsystem consists of one central RFM69 HCW radio (the radio hub) connected to a Raspberry Pi as illustrated below.  Additional slaved radio nodes are wired to ATmega 1284 microcontrollers (not shown).

<p align="center">
  <img src="/Images/raspberry-rfm69_pinout.png">
</p>

<p align="center">
  <img src="/Images/rfm69_pinout.png">
</p>

### Motor Controller Module:
Contains 2 DC Motors, Motor Driver, and Ultrasonic Sensor connected to the Raspberry Pi Zero W. The Motor Driver is connected to pins 8, 10, 19, 21, 36 and 38 which controls the 2 motors used in the system. The Ultrasonic sensor needs connection of trig and echo through pins 11 and 16 which is used to receive distance data. 

<p align="center">
  <img src="/Images/raspberryPi_pinout_motorController.png">
</p>

### Camera Module
- Plug the camera into the dedicated Raspberry Pi Camera slot.
- Enable the camera using raspi-config
```
sudo apt update
sudo apt full-upgrade
sudo raspi-config
```

## Running the System

### Sensor Module
Configure the sensor module as follows:

1. Add new publication paths
   - Insert new publication paths to temperatureHumidity.py to publish data to specific topics
   
1. Add new subscription paths and callback functions
   - Add subscription name to defines.py, which will auto-generate subscription path 
   - Open subscriptionFunctions.py and add callback functions for each subscription

### Radio Module
Configure the radio module as follows:

1. Open functionalizedRadio.py in the Source directory
   - Set node_id (from 1 - 255, by convention network hub is 1)
   - Set network_id (from 1 - 255)
   - Change key = "sampleEncryptKey" to a key of your chosing
   - Set testConfig = false
   
1. Open radio_hub.py
   - Configure JSONPayload to match expected inputs on radio network
   - Add/edit myMQTTClient.subscribe() functions to subscribe to other module's sensor data
   
1. Open subscriptionFunctions.py
   - Add callback functions for desired functionality
   


### Motor Controller Module


### Camera Module
There are two ways to run the camera module

1. Change to the UyTran/UnifiedExecution branch
   - Move to the Source directory
   -  `python main.py -c`


1. On the master branch
   - Modify the defines.py file by uncommenting the three camera section lines and commenting everything else out
   - Move to the Source directory
   - python main.py

