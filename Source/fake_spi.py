import fake_spidev as dummy

class fake_spi:

    def __init__(self): 
        self.dummy = dummy       

    def SpiDev():
        return dummy.fake_spidev

