import time
import threading
import copy
from rgbUtils.debug import debug

class BaseEffect(threading.Thread):

    # The Name and the Description of the Effect, 
    # should be overwritten by the inheritancing Effect
    name = "Undefined"
    desc = "No Description"

    # Something that will be used to show descriptions and value options 
    # of the parameters the effect will accept, in a way, that eg the webclient can decide, 
    # if the parameters can be toggeled by a button/checkbox/slider/whatever
    effectParameters = []

    stop = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.effectRGBStripList = []

    # when a strip is added or removed or the options change, the thread will not restart, 
    # the changes are pushed to the thread at livetime. so avoid log running loops without
    # accessing getRGBStrips and getEffectParams. It could happen, that a new effect for example already uses
    # a rgbStip while the loop of the old effect is running and has not got the changes.
    def run(self):
        self.effectParameterValues = []
        for effectParameterIndex, effectParameter in enumerate(self.effectParameters):
            self.effectParameterValues.append([])
            for option in effectParameter.options:
                self.effectParameterValues[effectParameterIndex].append(option[2])
        
        print(self.effectParameterValues)
        self.init()
        while not self.stop:
            # run the effect in endless while
            self.effect()
        self.end()
    
    # Init is called bevor the loop, use setEffectParams for init values 
    # and access them in the effect with getEffectParams
    def init(self):
        return

    # see run(): never save effectRGBStrips() as a variable and access it as often as possible
    # to avoid two effects accessing the rgbStrip
    def effect(self):
        while 1:
            debug("ET "+self.name+" effect() function needs to be replaced in inheritancing Effect")

    # called when the effect is stopped
    def end(self):
        return
    
    # when called the effect loop will stop and the thread can be terminated
    def stopEffect(self):
        self.stop = True

    # the effect itself will know its own strips. i don't know if it would be better if the effectController self 
    # should have this list, but then i must do something like nested arrays, naah. 
    def addRGBStrip(self,rgbStrip):
        self.effectRGBStripList.append(rgbStrip)
        self.onRGBStripAdded(rgbStrip)

    # remove a strip, if the effect has no more strips, the effect thread guardian will kill it
    def removeRGBStrip(self,rgbStrip):
        self.effectRGBStripList.remove(rgbStrip)

    # for overriding by the effect, when a strip is added
    def onRGBStripAdded(self,rgbStrip):
        return
    # for overriding by the effect, when a strip is added
    def onEffectParameterValuesUpdated(self):
        return

    # returns a list of the RGBStrips used by this effect
    def effectRGBStrips(self):
        return self.effectRGBStripList

    def addEffectParameter(self,effectParameter):
        self.effectParameters.append(effectParameter)

    # set Params as descriped in getParamsDescription()
    def updateEffectParameterValues(self,effectParameterIndex, effectParameterValues):
        print("updateEffectParameterValues",effectParameterIndex,effectParameterValues)
        for effectParameterValue in effectParameterValues:
            if self.effectParameters[int(effectParameterIndex)].testValue(int(effectParameterValue),int(effectParameterValues[effectParameterValue])):
                self.effectParameterValues[int(effectParameterIndex)][int(effectParameterValue)] = int(effectParameterValues[effectParameterValue])
        self.onEffectParameterValuesUpdated()