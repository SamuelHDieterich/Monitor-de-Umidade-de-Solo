#Code adapted from Martyn Wheeler
#https://github.com/martynwheeler/u-lora


from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
from machine import ADC, Pin
import utime

# Lora Parameters
RFM95_RST = 27
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 5
RFM95_INT = 28
RF95_FREQ = 868.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2


# use variables instead of numbers:
soil = ADC(Pin(26)) # Soil moisture PIN reference


# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)
while True:
    # read moisture value 
    moisture = soil.read_u16()
    data = '{0}'.format(moisture)
    tmp = lora.send_to_wait(data, SERVER_ADDRESS)
    print(moisture)
    print("sent", tmp)
    sleep(20)   




