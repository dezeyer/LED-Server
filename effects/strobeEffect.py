from rgbUtils.BaseEffect import BaseEffect
from rgbUtils.debug import debug
from random import randint
import time

class strobeEffect(BaseEffect):
    name = "strobeEffect"
    desc = "*Strobe*"

    def init(self):
        self.state = True

    #loop effect as long as not stopped
    def effect(self):
        y = -1
        x = -1
        if self.state:
            while x is y:
                x = randint(0,2)
            if x is 0:    
                for RGBStrip in self.effectRGBStrips():
                    RGBStrip.RGB(255,255,0)
            if x is 1:    
                for RGBStrip in self.effectRGBStrips():
                    RGBStrip.RGB(0,255,255)
            if x is 2:    
                for RGBStrip in self.effectRGBStrips():
                    RGBStrip.RGB(255,0,255)
            self.state = False
        else:
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(0,0,0)
            self.state = True
        time.sleep(0.01)
    
    # for overriding by the effect, when a strip is added
    def onRGBStripAdded(self,rgbStrip):
        return
        
    # for overriding by the effect, when a strip is added
    def onEffectParameterValuesUpdated(self):
        return