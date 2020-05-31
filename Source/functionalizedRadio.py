
# rfm radio---------------------------------------------------
from RFM69 import Radio, FREQ_915MHZ

# radio tranceiver configuration-------------------------------
# -------------------------------------------------------------
node_id = 1  # hub node (this)
network_id = 100  # 1 - 255
key = "sampleEncryptKey"  # must be shared accross all radios on the radio net


def initializeRadio():
    #radio = Radio(FREQ_915MHZ, node_id, network_id, key, True, False)#pytest -> works, fails for production
    radio = Radio(FREQ_915MHZ, node_id, network_id, encryptionKey=key, isHighPower=True, verbose=False)

    return radio
