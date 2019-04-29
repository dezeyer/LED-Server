from rgbUtils.BaseEffect import BaseEffect
from rgbUtils.debug import debug
import time

class rainbowEffect(BaseEffect):
    name = "rainbowEffect"
    desc = "LED-Band *sollte* rainbowEffect sein"

    def init(self):
        self.i=0
        self.speed = 1
        self.helligkeit = 100

    #loop effect as long as not stopped
    def effect(self):
        debug(self)
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*75):
            for rgbStrip in self.effectRGBStrips():
                for i in range(rgbStrip.STRIP_LENGHT):
                    color = self.wheel((i+j) & 255)
                    rgbStrip.WS2812b(i, color[0],color[1],color[2])
            for rgbStrip in self.effectRGBStrips():
                rgbStrip.show()
            time.sleep(100/1000.0)

        """Draw rainbow that uniformly distributes itself across all pixels.
        for j in range(256*iterations):
            for i in range(rgbStrip.STRIP_LENGHT):
                color = self.wheel(((i * 256 // rgbStrip.STRIP_LENGHT) + j) & 255)
                rgbStrip.WS2812b(i, color[0],color[1],color[2])
            #strip.show()
            time.sleep(wait_ms/1000.0)"""

        """Rainbow movie theater light style chaser animation.
        for j in range(256):
            for q in range(3):
                for rgbStrip in self.effectRGBStrips():
                    for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                        color=self.wheel((i+j) % 255)
                        rgbStrip.WS2812b(i+q, color[0],color[1],color[2])
              
                for rgbStrip in self.effectRGBStrips():
                    rgbStrip.show()
                time.sleep(50/1000.0)
                for rgbStrip in self.effectRGBStrips():
                    for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                        rgbStrip.WS2812b(i+q, 0,0,0)"""


        #if self.i < 3*255*self.speed:
        #    c = self.wheel_color(self.i,self.speed)
        #    #print("r: "+ str(round(c[0]/100*helligkeit,2))+" g: "+str(round(c[1]/100*helligkeit,2))+" b: "+str(round(c[2]/100*helligkeit,2)))
        #    for rgbStrip in self.effectRGBStrips():
        #        #print(c[0],c[1],c[2])
        #        rgbStrip.RGB(c[0],c[1],c[2],self.helligkeit)
        #    time.sleep(0.01)
        #    self.i =self.i +1
        #else:
        #    self.i=0
    
    # for overriding by the effect, when a strip is added
    def onRGBStripAdded(self,rgbStrip):
        return
        
    # for overriding by the effect, when a strip is added
    def onEffectParameterValuesUpdated(self):
        return
    
    def wheel_color(self,position,speed = 5):
        """Get color from wheel value (0 - 765)"""
        if position < 0:
            position = 0
        if position > 765*speed:
            position = 765*speed

        if position < (255*speed):
            r = (255*speed) - position % (255*speed)
            g = position % (255*speed)
            b = 0
        elif position < (510*speed):
            g = (255*speed) - position % (255*speed)
            b = position % (255*speed)
            r = 0
        else:
            b = (255*speed) - position % (255*speed)
            r = position % (255*speed)
            g = 0

        return [r/speed, g/speed, b/speed]

    # Define functions which animate LEDs in various ways.
    #https://github.com/jgarff/rpi_ws281x/blob/master/python/examples/SK6812_strandtest.py
    def colorWipe(self, rgbStrip, red, green, blue, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(rgbStrip.STRIP_LENGHT):
            rgbStrip.WS2812b(i, red,green,blue)
            time.sleep(wait_ms/1000.0)

    def theaterChase(self, rgbStrip , red, green, blue,  wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                    rgbStrip.WS2812b(i+q, red,green,blue)
                #strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                    rgbStrip.WS2812b(i+q, red,green,blue)

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return [pos * 3, 255 - pos * 3, 0]
        elif pos < 170:
            pos -= 85
            return [255 - pos * 3, 0, pos * 3]
        else:
            pos -= 170
            return [0, pos * 3, 255 - pos * 3]

    def rainbow(self, rgbStrip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(rgbStrip.STRIP_LENGHT):
                color = self.wheel((i+j) & 255)
                rgbStrip.WS2812b(i, color[0],color[1],color[2])
            #strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self,rgbStrip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(rgbStrip.STRIP_LENGHT):
                color = self.wheel(((i * 256 // rgbStrip.STRIP_LENGHT) + j) & 255)
                rgbStrip.WS2812b(i, color[0],color[1],color[2])
            #strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self,rgbStrip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                    color=self.wheel((i+j) % 255)
                    rgbStrip.WS2812b(i+q, color[0],color[1],color[2])
                #strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, rgbStrip.STRIP_LENGHT, 3):
                    rgbStrip.WS2812b(i+q, 0,0,0)

    # def wheel_color_2(self,r=255,g=0,b=0):
    #     if r<255:
    #         r=r+1
    #     elif g<255:
    #         g=g+1
    #     elif r=255:

    #     elif b<255:
    #         b=b+1
        