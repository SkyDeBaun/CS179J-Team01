class fake_spidev:

    def __init__(self):
        self.spidev = None

    def open(self, var1):
        print("Hello from fake spi.open")

    def xfer(self):
        print("Hello from fake spi.xfer")
        myList = [127]
        return myList

