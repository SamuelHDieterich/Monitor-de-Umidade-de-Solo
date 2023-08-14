#Code adapted from "Martyn Wheeler"
#https://github.com/martynwheeler/u-lora

#Based on code made by "Sachin Soni"
#https://github.com/techiesms/ESP32-Micropython-Series-Codes/tree/main/Episode%204

from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
import network
import time
import urequests
from .wifi_credentials import WIFI_CREDENTIALS

#Wifi connections 
timeout = 0
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(**WIFI_CREDENTIALS)


# This is our callback function that runs when a message is received
def on_recv(payload):
    #print("From:", payload.header_from)
    #print("Received:", payload.message)
    #print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    data_p = '{0}'.format(payload.message)
    r = urequests.post('https://httpbin.org/post', data = data_p)
    print(data_p)
    #print(r.text)
    print(r.json())
    

# Lora Parameters
RFM95_RST = 27
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 5
RFM95_INT = 28
RF95_FREQ = 868.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

# loop and wait for data
while True:   
    
    if not wifi.isconnected():
        print('connecting..')
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1)
            
    if(wifi.isconnected()):
        #print('Connected')

        # set callback
        lora.on_recv = on_recv

        # set to listen continuously
        lora.set_mode_rx()
        sleep(0.1)
    else:
        print('Time Out')
        print('Not Connected')
