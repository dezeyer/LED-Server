# import offEffect
from effects.offEffect import offEffect

from rgbUtils.debug import debug

from rgbUtils.BaseEffect import BaseEffect
from rgbUtils.RGBStrip import RGBStrip

import time
import threading
import os
import sys

#
# handles all the effects:
# - start/stop effects
# - changes parameters of specific effects
# - moves the rgbStrips to the effects
# - runs a guardian that detects dead effectThreads and moves Strips to offEffect
#
class effectController:

    # list of current running effects
    effectThreads = []

    offEffectThreadObject = None

    # maybe i will seperate this later
    onControllerChangeHandler = []

    def __init__(self,rgbStripController):
        self.rgbStripController = rgbStripController
        # load the effects
        self.effectsList = self.getEffectsListFromDir()
        # start the offEffect by default
        self.offEffectThreadObject = self.startEffect(offEffect,[])
        # - a bit of failover handling, remove dead threads from effectThread array
        # - move strips without an effect to the offEffect
        self.effectGuardian = self.effectGuardian(self)
        self.effectGuardian.start()

    # starts a effect by given class, rgbStrips and params ([[index,[param,param,param]],[index,[param,param,param]]])
    def startEffect(self, effectClass: BaseEffect, rgbStrips: list, params: list = []):
        newEffect = effectClass()
        newEffect.start()
        self.updateEffectParameters(newEffect, params)
        self.effectThreads.append(newEffect)

        for rgbStrip in rgbStrips:
            self.moveRGBStripToEffectThread(rgbStrip, newEffect)
        
        # if the effectThread has no strips, we stop it and remove it.
        if len(newEffect.effectRGBStrips()) == 0:
            newEffect.stopEffect()
            self.effectThreads.remove(newEffect)
        
        self.noticeControllerChange()
        return newEffect

    # returns all effectClasses but offEffect, since offEffect will never be killed
    # and should not be running twice
    def getEffects(self):
        # alle außer offEffect
        return self.effectsList

    # returns all running effectThreads
    def getEffectThreads(self):
        return self.effectThreads
        
    # returns a list of the RGBStrips used by this effect
    def getEffectRGBStrips(self, effectThreadObject: BaseEffect):
        return effectThreadObject.effectRGBStrips()

    # move a rgbStip to a running effectThread
    def moveRGBStripToEffectThread(self, rgbStrip: RGBStrip, effectThreadObject: BaseEffect):
        # cycle throught all effects and 
        # remove Strip from effect if added
        for et in self.effectThreads:
            if rgbStrip in et.effectRGBStrips():
                et.removeRGBStrip(rgbStrip)
        if effectThreadObject.isAlive():
            effectThreadObject.addRGBStrip(rgbStrip)
        # check if any effectThread has no more rgbStrips and if so, stop it

        # if the effectThread has no more strips, we stop it and remove it.
        for x, effectThread in enumerate(self.effectThreads):
            if len(effectThread.effectRGBStrips()) == 0 and x is not 0:
                effectThread.stopEffect()
                self.effectThreads.remove(effectThread)
        self.noticeControllerChange()
        
    # updates parameter of a running effectThread
    def updateEffectParameters(self, effectThreadObject: BaseEffect, effectParameters):
        for effectParameter in effectParameters:
            effectThreadObject.updateEffectParameterValues(
                effectParameter[0], effectParameter[1])
        self.noticeControllerChange()

    # stops all effectThreads and set the rgbStrips to off
    def stopAll(self):
        debug("effectController stopAll()")
        for effectThread in self.effectThreads:
            effectThread.stopEffect()
            debug("effectController killed "+str(effectThread))

        self.effectGuardian.stop()

        time.sleep(0.5)
        # GPIO.cleanup()

    # inform the controllerChangeHandler to update the client
    def noticeControllerChange(self):
        for controllerChangeHandler in self.onControllerChangeHandler:
            controllerChangeHandler()

    # add onControllerChangeHandler
    def addOnControllerChangeHandler(self, hander):
        print("addOnControllerChangeHandler", str(hander))
        self.onControllerChangeHandler.append(hander)
        # send data to this client
        hander()

    # remove onControllerChangeHandler
    def removeOnControllerChangeHandler(self, hander):
        print("removeOnControllerChangeHandler", str(hander))
        self.onControllerChangeHandler.remove(hander)

    # automaticly loads all modules from effects subdir and adds them to the list of effects if they have the BaseEffect as subclass 
    def getEffectsListFromDir(self):
        effectsList = []
        for raw_module in os.listdir(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir),"effects"))):
            
            if raw_module == '__init__.py' or raw_module == 'offEffect.py' or raw_module[-3:] != '.py':
                continue
            effectModule = __import__("effects."+raw_module[:-3], fromlist=[raw_module[:-3]])
            effectClass = getattr(effectModule, raw_module[:-3])
            if issubclass(effectClass,BaseEffect):
                effectsList.append(effectClass)
        print("Loaded effects: ",effectsList)
        return effectsList

    def onRGBStripRegistered(self,rgbStrip):
        self.offEffectThreadObject.addRGBStrip(rgbStrip)
        self.noticeControllerChange()

    def onRGBStripUnRegistered(self,rgbStrip):
        # cycle throught all effects and 
        # remove Strip from effect if added
        for et in self.effectThreads:
            if rgbStrip in et.effectRGBStrips():
                et.removeRGBStrip(rgbStrip)
        self.noticeControllerChange()

    class effectGuardian(threading.Thread):
        def __init__(self, effectController):
            threading.Thread.__init__(self)
            self.effectController = effectController
            self.stopped = False

        def run(self):
            while not self.stopped:
                for effectThread in self.effectController.effectThreads:                        
                    # if Thread was killed by something else, we remove it from the list
                    if not effectThread.isAlive():
                        for rgbStrip in effectThread.effectRGBStrips():
                            self.effectController.moveRGBStripToEffectThread(rgbStrip,self.effectController.offEffectThreadObject)
                        self.effectController.effectThreads.remove(effectThread)
                        print("effectController:effectGuardian removed dead Thread " +
                              str(effectThread) + ". There must be an error in code!")
                        self.effectController.noticeControllerChange()
                time.sleep(1)

        def stop(self):
            self.stopped = True
