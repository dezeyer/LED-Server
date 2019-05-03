
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from util.RGBStrip import RGBStrip as RGBStrip
from util.UDPListner import UDPListner as UDPListner
import sys

#use the BCM pin numbers here
rgbStrips = [
    #RGBStrip("Test Dahem", 4, 17 , 22),
    RGBStrip("Unter Theke", 20, 16 , 21),
    RGBStrip("Über Theke", 22, 13, 27),
    RGBStrip("Fensterbank", 5, 26, 6)
]
# set remote address and port
remoteaddr = ("192.168.0.255",8002)


udplistners = []
for rgbStrip in rgbStrips:
    udplistners.append(UDPListner(rgbStrip,remoteaddr))

while True:
    try:
        for udplistner in udplistners:
            udplistner.loop()
    except KeyboardInterrupt:
        for rgbStrip in rgbStrips:
            rgbStrip.stop()
        sys.exit()