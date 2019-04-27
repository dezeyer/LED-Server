from rgbUtils.BaseEffect import BaseEffect
from rgbUtils.debug import debug

import time

class offEffect(BaseEffect):
    name = "offEffect"
    desc = "LED-Band *sollte* nicht an sein"

    def effect(self):
        time.sleep(1)
        return
    
    # for overriding by the effect, when a strip is added
    def onRGBStripAdded(self,rgbStrip):
        rgbStrip.RGB(0,0,0,)
        return

    # for overriding by the effect, when a strip is added
    def onEffectParameterValuesUpdated(self):
        for RGBStrip in self.effectRGBStrips():
            RGBStrip.RGB(0,0,0)
        return