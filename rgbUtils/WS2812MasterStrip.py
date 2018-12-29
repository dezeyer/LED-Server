# The Master Strip that can be used as multiple RGBStrips or later as one for Special Effects
# see https://github.com/mdaffin/PyNeoPixel for arduino ino

import struct
import serial
import time


class WS2812MasterStrip:

    def __init__(self,port,LED_COUNT):

        #serial connection
        self.port = port
        self.ser = serial.Serial(self.port, 115200, timeout=1)
        self.command_count = 0

        self.LED_COUNT = LED_COUNT

        self.lock = False

        self.setPixelColorRange(1,LED_COUNT, 0, 0, 0)
        
    def setPixelColorRange(self, pixelstart, pixelstop, red, green, blue):
        # locking while sending serial data, because multiple threads 
        # could try to send data at the same time
        while self.lock:
            #time.sleep(0.001)
            return
        self.lock = True
        
        for pixel in  [pixelstart,pixelstop]:
            if pixelstart > self.LED_COUNT:
                print("WS2812MasterStrip@"+self.port+" Strip is only "+self.LED_COUNT+" pixels long")
                return
        pixelstart = pixelstart - 1
        pixelstop = pixelstop - 1
        message = struct.pack('>BBBHHBBB', ord(':'), self.command_count, ord('r'), pixelstart, pixelstop, red, green, blue)
        self.command_count += 1
        if self.command_count >=255:
            self.command_count = 0
        #print(message)
        self.ser.write(message)
        response = self.ser.readline()
        self.lock = False
        #print(response)