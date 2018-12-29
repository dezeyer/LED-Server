#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

#RGBStrip("Unter Theke",
            # wiringpi 24,-> BCM 19 -> GPIO. 24 -> kabel fehlt  
            # wiringpi 4, -> BCM 23 -> GPIO. 4  -> Mosfet LAHMT (rot)
            # wiringpi 0, -> BCM 17 -> GPIO. 0  -> Mosfet TOT   (weiß)
#RGBStrip("Über Theke",
            # wiringpi 3, -> BCM 22  -> GPIO. 3 
            # wiringpi 23,-> BCM 13 -> GPIO. 23
            # wiringpi 2, -> BCM 27 -> GPIO  2

#RGBStrip("Fensterbank",
            # wiringpi 21,-> BCM 5  -> GPIO. 21
            # wiringpi 25,-> BCM 26 -> GPIO. 25
            # wiringpi 22,-> BCM 6  -> GPIO. 22

#use the BCM pin numbers here
"""
from rgbUtils.RGBStrip import RGBStrip
rgbStrips = [
    #RGBStrip("Test Dahem", 4, 17 , 22),
    RGBStrip("Unter Theke", 20, 16 , 21),
    RGBStrip("Über Theke", 22, 13, 27),
    RGBStrip("Fensterbank", 5, 26, 6)
]

# setup PRi.GPIO
GPIO.setmode(GPIO.BCM)
# setup PWM for the rgbStrips
for RGBStrip in self.getRGBStrips():
    RGBStrip.init()

"""
"""
Use WS2812B Strips:
an arduino (uno tested) must be connected via usb while running 
the sketch in the root folder. Define the Strip as masterstrip and
use parts of it as a rgbStrip


"""

from rgbUtils.WS2812MasterStrip import WS2812MasterStrip
from rgbUtils.WS2812Strip import WS2812Strip
# LED_COUNT must be the same than in the arduino sketch
ws2812master = WS2812MasterStrip('/dev/ttyACM0',150)
rgbStrips = [
    WS2812Strip("LEDS 1-50",1,50,ws2812master),
    WS2812Strip("LEDS 51-100",51,100,ws2812master),
    WS2812Strip("LEDS 101-150",101,150,ws2812master),
]

"""
def drange(start, stop, step):
     r = start
     while r < stop:
         yield r
         r += step

rgbStrips = []
for x in drange(1,150,10):
    rgbStrips.append(WS2812Strip(str(x)+"-"+str(x),x,x,ws2812master))
"""

# int Port to bind. ports < 1024 need sudo access
SocketBindPort = 8000

# Maximum brightness of the RGB Strips Max Value is 100, can be set lower if the strips are too bright.
# (What I do not think, RGB Strips are never too bright)
# MaxBrightness = 100

# GPIO Pins that are working with pwm. At the moment A and B models only
# todo: check rpi version and add the missing pins if there are more that can be used
AllowedGPIOPins = [3, 5, 7, 8, 10, 11, 12, 13, 15, 19, 21, 22, 23, 24, 26]

BASE_PATH = path.dirname(path.realpath(__file__))
