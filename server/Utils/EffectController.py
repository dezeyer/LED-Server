# import offEffect

from Effects.OffEffect import OffEffect
from Utils.BaseEffect import BaseEffect

import time
import threading
import os
import sys

#TypeCheck
from typing import Type, List
from Utils.RGBStrip import RGBStrip
from Utils.RGBStripController import RGBStripController


class EffectController:
    '''
    the effectController handles the effects and pushes the values to the rgbStripContoller
    it also calls the backendProvider's onChange function when there are changes made on the effects:
    
     - start/stop effects
     - changes parameters of specific effects
     - moves the rgbStrips to the effects
     - runs a guardian that detects dead effectThreads and moves Strips to offEffect
    '''
    
    rememberRGBStripEffectThreads: dict = {}

    # list of current running effects
    effectThreads: List[BaseEffect] = []
    # the always running base effect
    offEffectThreadObject: BaseEffect
    # maybe i will seperate this later
    onControllerChangeHandler: List[Type[object]] = []
    #rgbStripController
    rgbStripController: RGBStripController
 
    def __init__(self,rgbStripController: RGBStripController) -> None:
        '''Init the EffectController with the RGBStripController'''
        self.rgbStripController = rgbStripController
        # load the effects
        self.effectsList: List[Type[BaseEffect]] = self.getEffectsListFromDir()
        # start the offEffect by default
        self.offEffectThreadObject = self.startEffect(OffEffect,[])
        
        # - a bit of failover handling, remove dead threads from effectThread array
        # - move strips without an effect to the offEffect
        self.effectGuardian = self.EffectGuardian(self)
        self.effectGuardian.start()

    
    def startEffect(self, effectClass: Type[BaseEffect], rgbStrips: list, params: list = []) -> BaseEffect: #TODO params as a object -> EffectParams
        '''starts a effect by given class, rgbStrips and params ([[index,[param,param,param]],[index,[param,param,param]]])'''
        newEffect = effectClass()
        if len(self.effectThreads) > 0 and len(rgbStrips) > 0 or len(self.effectThreads) == 0:
            newEffect.start()
            self.updateEffectParameters(newEffect, params)
            self.effectThreads.append(newEffect)

            for rgbStrip in rgbStrips:
                self.moveRGBStripToEffectThread(rgbStrip, newEffect)
            
        self.noticeControllerChange()
        return newEffect

    
    def getEffects(self) -> List[Type[BaseEffect]]:
        '''
        returns all effectClasses but offEffect, since offEffect will never be killed
        and should not be running twice
        '''
        # alle außer offEffect
        return self.effectsList

    
    def getEffectThreads(self) -> List[BaseEffect]:
        '''returns all running effectThreads'''
        return self.effectThreads
        
    
    def getEffectRGBStrips(self, effectThreadObject: BaseEffect) -> List[RGBStrip]:
        '''returns a list of the RGBStrips used by this effect'''
        return effectThreadObject.effectRGBStrips()

    
    def moveRGBStripToEffectThread(self, rgbStrip: RGBStrip, effectThreadObject: BaseEffect) -> None:
        '''move a rgbStip to a running effectThread'''
        # cycle throught all effects and 
        # remove Strip from effect if added
        for et in self.effectThreads:
            if rgbStrip in et.effectRGBStrips():
                et.removeRGBStrip(rgbStrip)
        if effectThreadObject.isAlive():
            self.rememberRGBStripEffectThreads[rgbStrip.STRIP_NAME] = et
            effectThreadObject.addRGBStrip(rgbStrip)
            
        # check if any effectThread has no more rgbStrips and if so, stop it
        # if the effectThread has no more strips, we stop it and remove it.
        for x, effectThread in enumerate(self.effectThreads):
            # but ignore the first effectthread, since that is our offeffect that should never be killed
            if len(effectThread.effectRGBStrips()) == 0 and x is not 0:
                effectThread.stopEffect()
                self.effectThreads.remove(effectThread)
        self.noticeControllerChange()
        
    
    def updateEffectParameters(self, effectThreadObject: BaseEffect, effectParameters: list):
        '''updates parameter of a running effectThread ([[index,[param,param,param]],[index,[param,param,param]]])'''
        for effectParameter in effectParameters:
            effectThreadObject.updateEffectParameterValues(
                effectParameter[0], effectParameter[1])
        self.noticeControllerChange()

    
    def stopAll(self):
        '''stops all effectThreads and set the rgbStrips to off'''
        print("effectController stopAll()")
        for effectThread in self.effectThreads:
            print("effectController killing... "+str(effectThread))
            effectThread.stopEffect()
            print("effectController killed "+str(effectThread))

        print("effectController stopping Guardian... ")
        self.effectGuardian.stop()
        print("effectController stopped Guardian")

        time.sleep(0.5)

    
    def noticeControllerChange(self) -> None:
        '''inform the controllerChangeHandler to update the client'''
        for controllerChangeHandler in self.onControllerChangeHandler:
            controllerChangeHandler()

    def addOnControllerChangeHandler(self, hander: Type[object]) -> None: #TODO class instead of function for OnControllerChangeHandler?
        '''add onControllerChangeHandler'''
        print("addOnControllerChangeHandler", str(hander))
        self.onControllerChangeHandler.append(hander)
        # send data to this client
        hander()

    
    def removeOnControllerChangeHandler(self, hander: Type[object]): #TODO class instead of function for OnControllerChangeHandler?
        '''remove onControllerChangeHandler'''
        print("removeOnControllerChangeHandler", str(hander))
        if hander in self.onControllerChangeHandler:
            self.onControllerChangeHandler.remove(hander)
        else:
            print('\n\n -> client was never registered!')

     
    def getEffectsListFromDir(self) -> List[Type[BaseEffect]]:
        '''automaticly loads all modules from effects subdir and adds them to the list of effects if they have the BaseEffect as subclass'''
        effectsList: List[Type[BaseEffect]] = []
        for raw_module in os.listdir(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir),"Effects"))):
            
            if raw_module == '__init__.py' or raw_module == 'OffEffect.py' or raw_module[-3:] != '.py':
                continue
            effectModule = __import__("Effects."+raw_module[:-3], fromlist=[raw_module[:-3]])
            effectClass = getattr(effectModule, raw_module[:-3])
            if issubclass(effectClass,BaseEffect):
                effectsList.append(effectClass)
        print("Loaded effects: ",effectsList)
        return effectsList

    
    def onRGBStripRegistered(self,rgbStrip: RGBStrip):
        ''' moves new rgbStrip to the offEffectThread and notice all Controller Clients'''
        if rgbStrip.STRIP_NAME in self.rememberRGBStripEffectThreads:
            restoredEffect: BaseEffect = self.rememberRGBStripEffectThreads[rgbStrip.STRIP_NAME]
            if restoredEffect.isAlive():
                print("stripname in rememberRGBStripEffectThreads -> same effect was never stopped, move to")
                self.moveRGBStripToEffectThread(rgbStrip,restoredEffect)
            else:                     
                print("stripname in rememberRGBStripEffectThreads -> create new effect")
                
                effectParamValueList: list = []
                for x in range(len(restoredEffect.effectParameterValues)):
                    valdict: dict = {}
                    for y in range(len(restoredEffect.effectParameterValues[x])):
                        valdict[y] = restoredEffect.effectParameterValues[x][y]
                    effectParamValueList.append([x,valdict])
                self.startEffect(restoredEffect.__class__,[rgbStrip],effectParamValueList)
            self.rememberRGBStripEffectThreads.pop(rgbStrip.STRIP_NAME)
           
            
        else:
            print("stripname was not in rememberRGBStripEffectThreads")
            self.offEffectThreadObject.addRGBStrip(rgbStrip)
        self.noticeControllerChange()

    def onRGBStripUnRegistered(self,rgbStrip: RGBStrip):
        '''
        cycle throught all effectThreadss and 
        remove Strip from effect if added
        '''
        et: BaseEffect
        for et in self.effectThreads:
            if rgbStrip in et.effectRGBStrips():
                et.removeRGBStrip(rgbStrip)
        # if the effectThread has no more strips, we stop it and remove it.
        for x, effectThread in enumerate(self.effectThreads):
            # but ignore the first effectthread, since that is our offeffect that should never be killed
            if len(effectThread.effectRGBStrips()) == 0 and x is not 0:
                effectThread.stopEffect()
                self.effectThreads.remove(effectThread)
        self.noticeControllerChange()

    def updateFttValues(self,ftt: tuple):
        ''' TODO this is a themorary funtion util a recorderController is build'''
        effectThread: BaseEffect
        for effectThread in self.effectThreads:
            effectThread.updateFttValues(ftt)
   
    class EffectGuardian(threading.Thread):
        '''
        a bit of failover handling, remove dead threads from effectThread array
        move strips without an effect to the offEffect

        This Guardian detects Effect Threads that are killed in some unnormal way
        This is not the procedere how effects are stoped
        Something went wrong when the guarian is removing dead threads!
        '''
        def __init__(self, effectController):
            threading.Thread.__init__(self, name='EffectGuardian')
            
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
