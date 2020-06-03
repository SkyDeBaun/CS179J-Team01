#fake radio for integration testing calls dummy functions here to avoid errors initializing the hardware
import sys, time, logging
from datetime import datetime
import logging

class Radio():

    def __init__(self, freq, ID, networkID, **kwargs):
        for key, value in kwargs.items(): #attempt to work around kwargs error during integration testing: possible test usage
            print ("%s == %s" %(key, value)) 

    def _init_gpio(self):
        self.hello = 0

    def _init_spi(self):
        self.hello = 0

    def _reset_radio(self):
        self.hello = 0

    def _set_config(self):
        self.hello = 0

    def Radio(self, var1, var2, var3, var4, var5):
        self.hello = 0

    def FREQ_915MHZ(self):
        self.hello = 0

    def _init_interrupt(self):
        self.hello = 0

    def __enter__(self):
        self.hello = 0

    def __exit__(self, *args):
        self.hello = 0

    def set_frequency(self, val):
        self.hello = 0

    def set_network(self, id):
        self.hello = 0

    def set_power_level(self):
        self.hello = 0

    def _send(self, to, buffer, val=False):
        self.hello = 0

    def broadcast(self):
        self.hello = 0

    def send(self, to, buff, **kwargs):
        self.hello = 0
