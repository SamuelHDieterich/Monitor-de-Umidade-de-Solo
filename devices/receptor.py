#  ____  _____ ____ _____ ____ _____ ___  ____
# |  _ \| ____/ ___| ____|  _ |_   _/ _ \|  _ \
# | |_) |  _|| |   |  _| | |_) || || | | | |_) |
# |  _ <| |__| |___| |___|  __/ | || |_| |  _ <
# |_| \_|_____\____|_____|_|    |_| \___/|_| \_\


# Code adapted from "Martyn Wheeler"
# https://github.com/martynwheeler/u-lora

# Based on code made by "Sachin Soni"
# https://github.com/techiesms/ESP32-Micropython-Series-Codes/tree/main/Episode%204



################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  BUILT-IN  ##
################

from utime import sleep, localtime
from ntptime import settime
import network
import json
import urequests


###############
## EXTERNAL  ##
###############

from .lib.ulora import LoRa



################################################################################
##                                  CONSTANTS                                 ##
################################################################################

from .config.wifi_credentials import WIFI_CREDENTIALS
from .config.lora_parameters import *
from .config.api import POST_RECEPTOR_STATUS, POST_COLLECTOR_RECORD

SLEEP_TIME = 60 # seconds



################################################################################
##                               CONFIGURATIONS                               ##
################################################################################

# Wifi connections
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_CREDENTIALS["ssid"], WIFI_CREDENTIALS["password"])

# LoRa initialisation
lora = LoRa(
  spi_channel=RFM95_SPIBUS,
  interrupt=RFM95_INT,
  this_address=SERVER_ADDRESS,
  cs_pin=RFM95_CS,
  reset_pin=RFM95_RST,
  freq=RF95_FREQ,
  tx_power=RF95_POW,
  acks=ACKS
)



################################################################################
##                                  FUNCTIONS                                 ##
################################################################################

# Format the local time to a string (RFC 3339)
def format_local_time() -> str:
  current_time = localtime()
  # Format the time to RFC 3339
  # YEAR"-"MONTH"-"DAY"T"HOUR":"MINUTE":"SECOND"Z"
  timestamp = "{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
    current_time[0], current_time[1], current_time[2],
    current_time[3], current_time[4], current_time[5]
  )
  return timestamp


# This is our callback function that runs when a message is received
def on_recv(message) -> None:

  # Format the body of the request
  data = dict(
    collection_date = format_local_time(),
    read_humidity = message.message,
  )

  # Send the request
  r = urequests.post(
    url=POST_COLLECTOR_RECORD.format(message.header_from), 
    data=json.dumps(data)
  )
  
  # Print the response
  print(r.json())


# Update the status of the receptor
def update_status() -> None:

  # Format the body of the request
  data = dict(
    update_date = format_local_time(),
    records_in_buffer = 0,# Dummy value for now
  )

  # Send the request
  r = urequests.post(
    url=POST_RECEPTOR_STATUS, 
    data=json.dumps(data)
  )
  
  # Print the response
  print(r.json())



################################################################################
##                                    MAIN                                    ##
################################################################################

# Set callback
lora.on_recv = on_recv

# Set to listen continuously
lora.set_mode_rx()

while True:

  # Check if the receptor is connected to the internet
  if not wifi.isconnected():
    print('Connecting to the internet...')
    while not wifi.isconnected():
      sleep(1)

  # Sincroniza o RTC do microcontrolador com o servidor NTP
  settime()

  # Update the status of the receptor
  update_status()

  # Sleep for a while
  sleep(SLEEP_TIME)