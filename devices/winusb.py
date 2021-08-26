# Copyright (c) 2021, RT-Thread Development Team
#
# SPDX-License-Identifier: Apache-2.0
#
# Change Logs:
# Date           Author       Notes
# 2021-08-26     liukang      the first version

import os
import time
import struct
import logging
import threading
import usb.core
import usb.util

LOG_LVL = logging.INFO
LOG_TAG = 'devices.usb'
logger = logging.getLogger(LOG_TAG)
logger.setLevel(LOG_LVL)


class UsbDev:
    def __init__(self):
        # 0x218a, 0x1f3a
        self.idProduct = 8586
        self.idVendor = 7994
        self.usb_dev = None
        self.interface = None
        self.inter_number = 0
        self.endpoint_in = 0
        self.endpoint_out = 0
        self.find_rtt_usb_dev()
        self.find_endpoint()
        logger.debug("{} {} {} {}".format(self.interface, self.inter_number, self.endpoint_in, self.endpoint_out))
        self.rev_lock = threading.Lock()
        self.send_lock = threading.Lock()
        self.rev_thread = threading.Thread(target=self.usb_rev, daemon=True, name="usb_rev")
        self.rev_thread.start()

    def find_rtt_usb_dev(self):
        self.usb_dev = usb.core.find(find_all=True)
        for usb_dev in self.usb_dev:
            if (usb_dev.idProduct != self.idProduct) and (usb_dev.idVendor != self.idVendor):
                continue
            if len(usb_dev.langids) == 0:
                continue

            cfg = usb_dev.get_active_configuration()
            for interface in cfg:
                # 02h CDC Communication
                # 0Ah CDC-Data Communication
                # FFh Vendor Specific
                if interface.bInterfaceClass != 0xFF:
                    continue
                else:
                    self.usb_dev = usb_dev
                    self.interface = interface
                    break

    def find_endpoint(self):
        ep_out = usb.util.find_descriptor(
            self.interface,
            # match the first OUT endpoint
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.endpoint_out = ep_out.bEndpointAddress

        ep_in = usb.util.find_descriptor(
            self.interface,
            # match the first IN endpoint
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
        self.endpoint_in = ep_in.bEndpointAddress
        self.inter_number = self.interface.bInterfaceNumber

    def usb_rev(self):
        buffer = usb.util.create_buffer(10240)
        logger.info("usb device is listening")
        while True:
            try:
                size = self.usb_dev.read(self.endpoint_in, buffer, timeout=10000000)
            except Exception as e:
                self.usb_dev.reset()
                logger.error(e)
                os.kill(os.getpid(), 9)
                return
            msg = buffer[:size]
            logger.debug("usb rev msg: {}, msg len: {}".format(msg, len(msg)))
            time.sleep(1)
            self.usb_send(msg)

    def usb_send(self, msg):
        size = len(msg)
        msg_len = struct.pack('<I', size)

        self.send_lock.acquire()
        try:
            self.usb_dev.ctrl_transfer(0x21, 0x0a, 0, self.inter_number, msg_len)
            self.usb_dev.write(self.endpoint_out, msg, timeout=1000)
        except Exception as e:
            self.send_lock.release()
            raise OSError(e)

        self.send_lock.release()
        logger.debug("usb send msg: {}, msg len: {}".format(msg, len(msg)))
