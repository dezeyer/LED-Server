import pyaudio
import numpy
import wave
import subprocess
#import matplotlib.pyplot as plt

numpy.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 32 # number of data points to read at a time
RATE = 44100 # time resolution of the recording device (Hz)

class SimpleBeatDetection:
    """
    Simple beat detection algorithm from
    http://archive.gamedev.net/archive/reference/programming/features/beatdetection/index.html
    """
    def __init__(self, history = 43):
        self.local_energy = numpy.zeros(history) # a simple ring buffer
        self.local_energy_index = 0 # the index of the oldest element

    def detect_beat(self, signal):

        samples = signal.astype(numpy.int) # make room for squares
        # optimized sum of squares, i.e faster version of (samples**2).sum()
        instant_energy = numpy.dot(samples, samples) / float(0xffffffff) # normalize

        local_energy_average = self.local_energy.mean()
        local_energy_variance = self.local_energy.var()

        beat_sensibility = (-0.0025714 * local_energy_variance) + 1.15142857
        beat = instant_energy > beat_sensibility * local_energy_average

        self.local_energy[self.local_energy_index] = instant_energy
        self.local_energy_index -= 1
        if self.local_energy_index < 0:
            self.local_energy_index = len(self.local_energy) - 1

        return beat

sb = SimpleBeatDetection()

p=pyaudio.PyAudio() # start the PyAudio class
# for i in range(p.get_device_count()):     
#     devinfo = p.get_device_info_by_index(i)
#     print(i,devinfo["name"])


stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

while True: 
    data = stream.read(CHUNK)
    signal = numpy.frombuffer(data, numpy.int16)
    if(sb.detect_beat(signal)):
        i+1
        print(i,"Beat!")

stream.stop_stream()
stream.close()
p.terminate()