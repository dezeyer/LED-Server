from Utils.BaseEffect import BaseEffect
from Utils.RGBStrip import RGBStrip
from Utils.EffectParameter import slider, colorpicker
import time

import sys
import numpy
from time import perf_counter, sleep
from random import randint, shuffle

import typing

import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg') # THIS MAKES IT FAST!
matplotlib.get_backend()

class MusikEffect2(BaseEffect):
    name = "musikEffect2"
    desc = "LED-Band *sollte* nach musik blinken"
    
    
    
    # Something that will be used to show descriptions and value options 
    # of the parameters the effect will accept, in a way, that eg the webclient can decide, 
    # if the parameters can be toggeled by a button/checkbox/slider/whatever
    """radio( 
        "Shuffle LED to Freq Order",
        "Off -> Mapping  ",
        [
            [0,255,255,"red"],
            [0,255,255,"green"],
            [0,255,255,"blue"]
        ]
    ),"""
    effectParameters: list = [
        slider(
            "Effect Brightnes",
            "Choose a brightness for your LED's",
            [
                 [0,100,100,"brightness"],
             ]
         )
    ]

    def init(self):
        
        
        self.fft_random_keys = [0,1,2,3]
        self.fft_random = [0,0,0,0]

        self.y_max_freq_avg_list = [0]
        self.low_freq_avg_list = [0]
        self.bpm_list = []
        self.prev_beat = 0 # timestamp

        '''
        self.fig = plt.gcf()
        
        self.fig.show()
        '''
        return


    #loop effect as long as not stopped
    def effect(self):
        '''plt.clf()
        #plt.ylim(-.5, numpy.amax(self.y_max_freq_avg_list))
        plt.xlabel('xs')
        plt.ylabel('ys')
        plt.plot(self.ftt[0],self.ftt[1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()'''
        self.plot_audio_and_detect_beats()
        #self.freqtocolor()
        #if(time.time() - self.lastTime >= 0.002):
        #for RGBStrip in self.effectRGBStrips():
        #    r= RGBStrip.red-1
        #    if(r<0):
        #        r=0
        #    g= RGBStrip.green-1
        #    if(g<0):
        #        g=0
        #    b= RGBStrip.blue-1 
        #    if(b<0):
        #        b=0
        #    RGBStrip.RGB(r,g,b)
        #self.lastTime = time.time()
        sleep(0.00833333333)

    def end(self):
        pass

    def plot_audio_and_detect_beats(self):
        if not self.hasNewFttValues: 
            return

        # get x and y values from FFT
        xs, ys = self.ftt

        amax = numpy.amax(ys)
        if amax > 0:
            self.y_max_freq_avg_list.append(amax)
        if len(self.y_max_freq_avg_list ) > 50000:
            self.y_max_freq_avg_list = self.y_max_freq_avg_list[25000:]

        calc = numpy.amax(ys) / numpy.amax(self.y_max_freq_avg_list) * 765
        """print(amax)
        print(numpy.amax(self.y_max_freq_avg_list))
        print(calc)
        print("-----------")
        """
        c: self.Color = self.pitchRainbow(calc)
        rgbStrip: RGBStrip
        for rgbStrip in self.effectRGBStrips():
            """
            for i in range(rgbStrip.STRIP_LENGHT):
                if rgbStrip.STRIP_LENGHT-1-10 is not i:
                    rgbStrip.WS2812b(rgbStrip.STRIP_LENGHT-i-1, rgbStrip.red[rgbStrip.STRIP_LENGHT-i-2], rgbStrip.green[rgbStrip.STRIP_LENGHT-i-2], rgbStrip.blue[rgbStrip.STRIP_LENGHT-i-2])
                else:
                    rgbStrip.WS2812b(rgbStrip.STRIP_LENGHT-i-1, c.red, c.green, c.blue)
            rgbStrip.show()
            """
            rgbStrip.RGB(int(c.red),int(c.green),int(c.blue))
        # shorten the cumulative list to account for changes in dynamics
        
            
    def pitchRainbow(self,p: float):
        if p < 1:
            return self.Color(0,0,0)
        elif p < 255:
            return self.Color(255 - p % 255,p % 255,0)
        elif p < 510:
            return self.Color(0,255 - p % 255,p % 255)
        else:
            return self.Color(p % 255,0,255 - p % 255)

    def pitchConv(self,p: float):

        r:float
        g:float
        b:float

        if p < 40:
            return self.Color(255,0,0)
        
        elif p >= 40 and p <= 77 : 
            b = (p - 40) * (255/37.0000)
            return self.Color(255,0,b)
        
        elif p > 77 and p <= 205:
            r = 255 - ((p - 78) * 2)
            return self.Color(r,0,255)
        
        elif p >= 206 and p <= 238:
            g = (p - 206) * (255/32.0000)
            return self.Color(0,g,255)
        
        elif p <= 239 and p <= 250:
            r = (p - 239) * (255/11.0000)
            return self.Color(r, 255, 255)
        
        elif p >= 251 and p <= 270:
            return self.Color(255, 255, 255)
        
        elif p >= 271 and p <= 398:
            rb = 255-((p-271)*2)
            return self.Color(rb, 255, rb)
        
        elif p >= 398 and p <= 650:
            return self.Color(0, 255-(p-398), (p-398))
        
        else:
            return self.Color(255, 0, 0)
        

    class Color:
        red: float 
        green: float
        blue: float
        def __init__(self,red:float,green:float,blue:float) -> None:
            self.red = red
            self.green = green
            self.blue = blue