#   ____ ___  _     _     _____ ____ _____ ___  ____
#  / ___/ _ \| |   | |   | ____/ ___|_   _/ _ \|  _ \
# | |  | | | | |   | |   |  _|| |     | || | | | |_) |
# | |__| |_| | |___| |___| |__| |___  | || |_| |  _ <
#  \____\___/|_____|_____|_____\____| |_| \___/|_| \_\


# Code adapted from "Martyn Wheeler"
# https://github.com/martynwheeler/u-lora



################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  BUILT-IN  ##
################

from utime import sleep, localtime
from machine import ADC, Pin


###############
## EXTERNAL  ##
###############

from .lib.ulora import LoRa



################################################################################
##                                  CONSTANTS                                 ##
################################################################################

from .config.lora_parameters import *

SLEEP_TIME = 20 # seconds



################################################################################
##                               CONFIGURATIONS                               ##
################################################################################

# Humidity sensor
soil = ADC(Pin(26)) # Soil moisture PIN reference

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
##                                    MAIN                                    ##
################################################################################

while True:

  # Read moisture value
  moisture = soil.read_u16()

  # Send data to gateway
  result = lora.send_to_wait(str(moisture), SERVER_ADDRESS)

  # Print result
  print("Moisture: {}", moisture)
  print("Sent: {}", result)

  # Sleep for a while
  sleep(SLEEP_TIME)
  