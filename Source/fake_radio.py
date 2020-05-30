import sys, time, logging
from datetime import datetime
import logging
#import spidev
#import RPi.GPIO as GPIO
#from registers import *
#from packet import Packet
#from config import get_config


class Radio():

    def __init__(self, freq, ID, networkID, **kwargs):
        for key, value in kwargs.items(): 
            print ("%s == %s" %(key, value)) 

    def _init_gpio(self):
        self.hello = 1

    def _init_spi(self):
        self.hello = 2

    def _reset_radio(self):
        self.hello = 3

    def _set_config(self):
        self.hello = 3

    def Radio(self, var1, var2, var3, var4, var5):
        self.hello = 3

    def FREQ_915MHZ(self):
        self.hello = 3

    def _init_interrupt(self):
        self.hello = 3

    def __enter__(self):
        self.hello = 3

    def __exit__(self, *args):
        self.hello = 3

    def set_frequency(self, val):
        self.hello = 3

    def set_network(self, id):
        self.hello = 3

    def set_power_level(self):
        self.hello = 3

    def _send(self, to, buffer, val=False):
        self.hello = 3

    def broadcast(self):
        self.hello = 3

    def send(self, to, buff, **kwargs):
        self.hello = 3
