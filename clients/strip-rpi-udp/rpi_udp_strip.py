
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from util.UDPListner import UDPListner as UDPListner
import config
import sys

udplistners = []

for rgbStrip in config.rgbStrips:
    udplistners.append(UDPListner(rgbStrip,config.remoteaddr))

while True:
    try:
        for udplistner in udplistners:
            udplistner.loop()
    except KeyboardInterrupt:
        for rgbStrip in config.rgbStrips:
            rgbStrip.stop()
        sys.exit()