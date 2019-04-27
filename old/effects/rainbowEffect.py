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
        if self.i < 3*255*self.speed:
            c = self.wheel_color(self.i,self.speed)
            #print("r: "+ str(round(c[0]/100*helligkeit,2))+" g: "+str(round(c[1]/100*helligkeit,2))+" b: "+str(round(c[2]/100*helligkeit,2)))
            for rgbStrip in self.effectRGBStrips():
                #print(c[0],c[1],c[2])
                rgbStrip.RGB(c[0],c[1],c[2],self.helligkeit)
            time.sleep(0.05)
            self.i =self.i +1
        else:
            self.i=0
    
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

    # def wheel_color_2(self,r=255,g=0,b=0):
    #     if r<255:
    #         r=r+1
    #     elif g<255:
    #         g=g+1
    #     elif r=255:

    #     elif b<255:
    #         b=b+1
        