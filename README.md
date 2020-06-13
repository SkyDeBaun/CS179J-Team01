# CS179J - Senior Design Project

# Extensible Sensor Network

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
Use a `git clone` or download this repository
Activate your Python virtualenv
Navigate to the base directory of this repository on your device
Run `pip install -r requirements.txt`

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
Plug the camera into the dedicated Raspberry Pi Camera slot.
Enable the camera using raspi-config
```
sudo apt update
sudo apt full-upgrade
sudo raspi-config
```

## Running the System

### Camera Module
There are two ways to run the camera module

 - Change to the UyTran/UnifiedExecution branch
   - Move to the Source directory
   - 'python main.py -c'

 - On the master branch
   - Modify the defines.py file 

