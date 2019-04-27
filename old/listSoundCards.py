#! /usr/bin/env python

import sys
import time
import pyaudio

p=pyaudio.PyAudio() # start the PyAudio class
for i in range(p.get_device_count()):     
    devinfo = p.get_device_info_by_index(i)
    print(i,devinfo["name"])