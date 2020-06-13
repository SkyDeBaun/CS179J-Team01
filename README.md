# CS179J - Senior Design Project

## Extensible Sensor Network

## AWS Setup
### This project utilizes Amazon Web Services IoT Core to securely connect and facilitate communications between devices and the cloud using the MQTT messaging protocol.

-item Create an AWS account
-item Create IAM user accounts to manage access controls (if needed)
-item Select Region providing desired services (Oregon offers the most features)
-item Create and configure device Things (includes x.509 secure certificates)
-item Download secure certificates for project “Certificates” directory
-item Create and configure AWS Rules and/or Lambdas (as needed)


## Python Dependencies
Project has only been tested for Python 3.6+
We recommend that you set up a python virtual environment before continuing

## Project Installation
Use a `git clone` or download this repository
Activate your Python virtualenv
Navigate to the base directory of this repository on your device
Run `pip install -r requirements.txt`

## Hardware Setup

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


Change to the UyTran/UnifiedExecution branch
Move to the Source directory
`python main.py -c’
On the master branch
Modify the defines.py file 

