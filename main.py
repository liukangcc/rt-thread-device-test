import logging
import time
from devices.winusb import UsbDev

LOG_LVL = logging.INFO
LOG_TAG = 'main'
logger = logging.getLogger(LOG_TAG)
logger.setLevel(LOG_LVL)

logging.basicConfig(level=LOG_LVL, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt=None)

logger.info("winusb test start")
usb_test = UsbDev()

while True:
    time.sleep(10)


