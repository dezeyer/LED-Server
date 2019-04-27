from rgbUtils.BaseEffect import BaseEffect
from rgbUtils.EffectParameter import slider, colorpicker
from rgbUtils.debug import debug
import time

import sys
import numpy
from rgbUtils.pyAudioRecorder import pyAudioRecorder
from time import perf_counter, sleep
from random import randint, shuffle

class musikEffect(BaseEffect):
    name = "musikEffect"
    desc = "LED-Band *sollte* nach musik blinken"
    
    
    
    # Something that will be used to show descriptions and value options 
    # of the parameters the effect will accept, in a way, that eg the webclient can decide, 
    # if the parameters can be toggeled by a button/checkbox/slider/whatever
    effectParameters = [
    #     radio(\   
    #         "Shuffle LED to Freq Order",\
    #         "Off -> Mapping  ",\
    #         [\
    #             [0,255,255,"red"],\
    #             [0,255,255,"green"],\
    #             [0,255,255,"blue"]\
    #         ]\
    #     ),\
    #     slider(\
    #         "Effect Brightnes",\
    #         "Choose a brightness for your LED's",\
    #         [\
    #             [0,100,100,"brightness"],\
    #         ]\
    #     )\
    ]

    def init(self):

        self.fft_random_keys = [0,1,2,3]
        self.fft_random = [0,0,0,0]

        # used by strobe() 
        self.lastmode = 0

        self.recorderClient = pyAudioRecorder.recorderClient()
        self.rgbStripController.pyAudioRecorder.registerRecorderClient(self.recorderClient)

        return

    #loop effect as long as not stopped
    def effect(self):
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
        sleep(.001)

    def end(self):
       self.rgbStripController.pyAudioRecorder.unregisterRecorderClient(self.recorderClient)

    def plot_audio_and_detect_beats(self):
        if not self.rgbStripController.pyAudioRecorder.has_new_audio: 
            return

        # get x and y values from FFT
        xs, ys = self.rgbStripController.pyAudioRecorder.fft()

        # calculate average for all frequency ranges
        y_avg = numpy.mean(ys)
        
        

        #low_freq = numpy.mean(ys[20:47])
        #mid_freq = numpy.mean(ys[88:115])
        #hig_freq = numpy.mean(ys[156:184])
        
        low_freq = numpy.mean(ys[0:67])
        mid_freq = numpy.mean(ys[68:135])
        hig_freq = numpy.mean(ys[136:204])
        
        #get the maximum of all freq
        if len(self.y_max_freq_avg_list) < 250 or y_avg > 10 and numpy.amax([low_freq,mid_freq,hig_freq])/2 > numpy.amin(self.y_max_freq_avg_list):
            self.y_max_freq_avg_list.append(numpy.amax([low_freq,mid_freq,hig_freq]))
        
        y_max = numpy.amax(self.y_max_freq_avg_list)
        
        #y_max = numpy.mean([numpy.amax(ys),y_max])
        #print(low_freq,mid_freq,hig_freq,y_max)

        for i,item in enumerate([low_freq,mid_freq,hig_freq]):
            if item is None:
                item = 0

        low = round(low_freq/(y_max+10)*255)
        mid = round(mid_freq/(y_max+10)*255)
        hig = round(hig_freq/(y_max+10)*255)
        #print(low,mid,hig,y_max, numpy.amax(ys), y_avg)
        #print("------")

        self.fft_random[self.fft_random_keys[0]] = low
        self.fft_random[self.fft_random_keys[1]] = mid
        self.fft_random[self.fft_random_keys[2]] = hig
        self.fft_random[self.fft_random_keys[3]] = 0

        # calculate low frequency average
        #low_freq = [ys[i] for i in range(len(xs)) if xs[i] < 1000]
        low_freq = ys[0:47]
        low_freq_avg = numpy.mean(low_freq)
        
        if len(self.low_freq_avg_list) < 250 or low_freq_avg > numpy.amin(self.low_freq_avg_list)/2:
            self.low_freq_avg_list.append(low_freq_avg)
        cumulative_avg = numpy.mean(self.low_freq_avg_list)
        
        bass = low_freq[:int(len(low_freq)/2)]
        bass_avg = numpy.mean(bass)
        #print("bass: {:.2f} vs cumulative: {:.2f}".format(bass_avg, cumulative_avg))
        
        # check if there is a beat
        # song is pretty uniform across all frequencies
        if (y_avg > y_avg/5 and (bass_avg > cumulative_avg * 1.8  or (low_freq_avg < y_avg * 1.2 and bass_avg > cumulative_avg))):
            #self.prev_beat
            curr_time = perf_counter()
                
            # print(curr_time - self.prev_beat)
            if curr_time - self.prev_beat > 60/360*2: # 180 BPM max
                shuffle(self.fft_random_keys)
                
                # change the button color
                #self.beats_idx += 1
                #self.strobe()
                #print("beat {}".format(self.beats_idx))
                #print("bass: {:.2f} vs cumulative: {:.2f}".format(bass_avg, cumulative_avg))
                
                #print(self.fft_random)
                # change the button text
                bpm = int(60 / (curr_time - self.prev_beat))
                if len(self.bpm_list) < 4:
                    if bpm > 60:
                        self.bpm_list.append(bpm)
                else:
                    bpm_avg = int(numpy.mean(self.bpm_list))
                    if abs(bpm_avg - bpm) < 35:
                        self.bpm_list.append(bpm)
                    print("bpm: {:d}".format(bpm_avg))
                
                # reset the timer
                self.prev_beat = curr_time
        if y_avg > 10:
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(
                    self.fft_random[0],
                    self.fft_random[1],
                    self.fft_random[2]
                )
        
        # shorten the cumulative list to account for changes in dynamics
        if len(self.low_freq_avg_list) > 500:
            self.low_freq_avg_list = self.low_freq_avg_list[250:]
            #print("REFRESH!!")
        
        # shorten the cumulative list to account for changes in dynamics
        if len(self.y_max_freq_avg_list ) > 500:
            self.y_max_freq_avg_list = self.y_max_freq_avg_list[250:]
            print("--REFRESH y_max_freq_avg_list")

        # keep two 8-counts of BPMs so we can maybe catch tempo changes
        if len(self.bpm_list) > 24:
            self.bpm_list = self.bpm_list[8:]

        # reset song data if the song has stopped
        if y_avg < 10:
            self.bpm_list = []
            self.low_freq_avg_list = []
            print("new song")
            self.off()

        self.rgbStripController.pyAudioRecorder.newAudio = False
        # print(self.bpm_list)

    def strobe(self):
        x = randint(0,5)
        while x is self.lastmode:
            x = randint(0,5)

        self.lastmode = x
        r = 255#randint(0,255)
        g = 255#randint(0,255)
        b = 255#randint(0,255)
        if x is 0:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(r,g,0)
        if x is 1:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(0,g,b)
        if x is 2:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(r,0,b)
        if x is 3:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(r,0,0)
        if x is 4:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(0,g,0)
        if x is 5:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(0,0,b)
        if x is 6:    
            for RGBStrip in self.effectRGBStrips():
                RGBStrip.RGB(r,g,b)

    def off(self):
        for RGBStrip in self.effectRGBStrips():
            RGBStrip.RGB(0,0,0)

    def left_rotate(self,arr):
        if not arr:
            return arr
        
        left_most_element = arr[0]
        length = len(arr)
        
        for i in range(length - 1):
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
        
        arr[length - 1] = left_most_element
        return arr