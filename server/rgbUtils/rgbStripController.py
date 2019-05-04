from rgbUtils.RGBStrip import RGBStrip
import time
import threading
import json
class rgbStripController():
    def __init__(self):
        #threading.Thread.__init__(self)
        self.rgbStrips = []
        self.onRGBStripRegisteredHandler = []
        self.onRGBStripUnRegisteredHandler = []

    def registerRGBStrip(self,rgbStripName,onValuesUpdateHandler,ledcount=1):
        # maybe we can use an unique id if the strip reconnects later, eg push the uid
        # to the client on first connect and if he reconnects he sould send it back again.
        # the wmos could use the mac adress, if there is a python script it can save the uid
        # in a file or so.
        strip = RGBStrip(rgbStripName,onValuesUpdateHandler,ledcount)
        self.rgbStrips.append(strip)
        self.noticeRGBStripRegisteredHandler(strip)
        return strip

    def unregisterRGBStrip(self,strip):
        self.rgbStrips.remove(strip)
        self.noticeRGBStripUnRegisteredHandler(strip)

    # returns all registered rgbStips
    def getRGBStrips(self):
        return self.rgbStrips

    # inform all onRGBStripRegisteredHandler about the new RGBStrip
    def noticeRGBStripRegisteredHandler(self,rgbStrip):
        for hander in self.onRGBStripRegisteredHandler:
            hander(rgbStrip)

    # add onRGBStripRegisteredHandler
    def addOnRGBStripRegisteredHandler(self, function):
        self.onRGBStripRegisteredHandler.append(function)

    # remove onRGBStripRegisteredHandler
    def removeOnRGBStripRegisteredHandler(self, function):
        self.onRGBStripRegisteredHandler.remove(function)
    
    # inform all onRGBStripUnRegisteredHandder about the removed RGBStrip
    def noticeRGBStripUnRegisteredHandler(self,rgbStrip):
        for hander in self.onRGBStripUnRegisteredHandler:
            hander(rgbStrip)

    # add onRGBStripUnRegisteredHandler
    def addOnRGBStripUnRegisteredHandler(self, function):
        self.onRGBStripUnRegisteredHandler.append(function)

    # remove onRGBStripUnRegisteredHandler
    def removeOnRGBStripUnRegisteredHandler(self, function):
        self.onRGBStripUnRegisteredHandler.remove(function)