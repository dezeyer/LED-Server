from Utils.BaseEffect import BaseEffect
from Utils.EffectParameter import slider, colorpicker
import time

class OnEffect(BaseEffect):
    name = "onEffect"
    desc = "LED-Band *sollte* an sein"
    
    # Something that will be used to show descriptions and value options 
    # of the parameters the effect will accept, in a way, that eg the webclient can decide, 
    # if the parameters can be toggeled by a button/checkbox/slider/whatever
    effectParameters = [
        colorpicker(\
            "Effect Color",\
            "Choose a color for your LED's",\
            [\
                [0,255,255,"red"],\
                [0,255,255,"green"],\
                [0,255,255,"blue"]\
            ]\
        ),\
        slider(\
            "Effect Brightnes",\
            "Choose a brightness for your LED's",\
            [\
                [0,100,100,"brightness"],\
            ]\
        )\
    ]

    def init(self):
        return

    #loop effect as long as not stopped
    def effect(self):
        time.sleep(1)
        return

    # for overriding by the effect, when a strip is added
    def onRGBStripAdded(self,rgbStrip):
        rgbStrip.RGB(\
            # colorpicker red currentvalue
            self.effectParameterValues[0][0],\
            # colorpicker green currentvalue
            self.effectParameterValues[0][1],\
            # colorpicker blue currentvalue
            self.effectParameterValues[0][2],\
            # slider brightness currentvalue
            self.effectParameterValues[1][0]\
        )
        return

    # for overriding by the effect, when a params are updated
    def onEffectParameterValuesUpdated(self):
        for RGBStrip in self.effectRGBStrips():
            #print(self.effectParameterValues)
            RGBStrip.RGB(\
                # colorpicker red currentvalue
                self.effectParameterValues[0][0],\
                # colorpicker green currentvalue
                self.effectParameterValues[0][1],\
                # colorpicker blue currentvalue
                self.effectParameterValues[0][2],\
                # slider brightness currentvalue
                self.effectParameterValues[1][0]\
            )