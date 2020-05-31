
# rfm radio---------------------------------------------------
from RFM69 import Radio, FREQ_915MHZ

# radio tranceiver configuration-------------------------------
# -------------------------------------------------------------
node_id = 1  # hub node (this)
network_id = 100  # 1 - 255
key = "sampleEncryptKey"  # must be shared accross all radios on the radio net

testConfig = False

def initializeRadio():
    if testConfig:
        radio = Radio(FREQ_915MHZ, node_id, network_id, key, True, False)# use for pytest -> fails for production
    else:
        radio = Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False) #use for production -> kwargs fails for pytest

    return radio
