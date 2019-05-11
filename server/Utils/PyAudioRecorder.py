#
# The idea is to have only one thread accessing the audio input source instead
# of every music enabled thread itself. also, different fuctions calculating
# frequencys and so on shoud run in own threads to the leds get more updates
#
# in history one thread was calculating bpm, freqence average and max values in one thread
# before updating the leds, what the pi was a bit slow for and you cloud count every update 
# of the leds

# i think most of it is from https://github.com/shunfu/python-beat-detector/


import numpy
import pyaudio
import threading

import time


class PyAudioRecorder:
    """Simple, cross-platform class to record from the default input device."""

    def __init__(self):
        self.RATE = 44100
        self.BUFFERSIZE = 2**12
        self.secToRecord = .1
        self.kill_threads = False
        self.has_new_audio = False
        self.setup()

        # since the server only can handly one input (for now) this thread will calculate
        # some basic things for the musicEffectsThreads, so they can update the leds more often.
        # it is always posible to catch the fft() function and do your own thing in your musikEffect.

        # calculate bpm, this is the same for all clientThreads
        self.beats_idx = 0

        self.bpm_list = []
        self.prev_beat = time.perf_counter()
        self.low_freq_avg_list = []

        self.lastTime = time.time()
        

        self.recorderClients = []

    def setup(self):
        self.buffers_to_record = int(
            self.RATE * self.secToRecord / self.BUFFERSIZE)
        if self.buffers_to_record == 0:
            self.buffers_to_record = 1
        self.samples_to_record = int(self.BUFFERSIZE * self.buffers_to_record)
        self.chunks_to_record = int(self.samples_to_record / self.BUFFERSIZE)
        self.sec_per_point = 1. / self.RATE

        self.p = pyaudio.PyAudio()
        # start the PyAudio class
        for i in range(self.p.get_device_count()):
            devinfo = self.p.get_device_info_by_index(i)
            print(i, devinfo["name"])
        # make sure the default input device is broadcasting the speaker output
        # there are a few ways to do this
        # e.g., stereo mix, VB audio cable for windows, soundflower for mac
        self.in_stream = self.p.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=self.RATE,
                                     input=True,
                                     frames_per_buffer=self.BUFFERSIZE)
        print("Using default input device: {:s}".format(
            self.p.get_default_input_device_info()['name']))

        self.audio = numpy.empty(
            (self.chunks_to_record * self.BUFFERSIZE), dtype=numpy.int16)

    def close(self):
        print("pyAudioRecorder closed")
        self.kill_threads = True
        self.p.close(self.in_stream)

    ### RECORDING AUDIO ###

    def get_audio(self):
        """get a single buffer size worth of audio."""
        audio_string = self.in_stream.read(self.BUFFERSIZE)
        return numpy.fromstring(audio_string, dtype=numpy.int16)

    def record(self):
        while not self.kill_threads:
            for i in range(self.chunks_to_record):
                self.audio[i*self.BUFFERSIZE:(i+1)
                           * self.BUFFERSIZE] = self.get_audio()
            self.has_new_audio = True

    def start(self):
        print("pyAudioRecorder started")
        self.t = threading.Thread(target=self.record)
        self.t.start()

    ### MATH ###

    def downsample(self, data, mult):
        """Given 1D data, return the binned average."""
        overhang = len(data) % mult
        if overhang:
            data = data[:-overhang]
        data = numpy.reshape(data, (len(data) / mult, mult))
        data = numpy.average(data, 1)
        return data

    def fft(self, data=None, trim_by=10, log_scale=False, div_by=100):
        if not data:
            data = self.audio.flatten()
        left, right = numpy.split(numpy.abs(numpy.fft.fft(data)), 2)
        ys = numpy.add(left, right[::-1])
        if log_scale:
            ys = numpy.multiply(20, numpy.log10(ys))
        xs = numpy.arange(self.BUFFERSIZE/2, dtype=float)
        if trim_by:
            i = int((self.BUFFERSIZE/2) / trim_by)
            ys = ys[:i]
            xs = xs[:i] * self.RATE / self.BUFFERSIZE
        if div_by:
            ys = ys / float(div_by)
        return xs, ys

    ### multithreading things ###

    def registerRecorderClient(self,recorderClient):
        self.recorderClients.append(recorderClient)

    def unregisterRecorderClient(self,recorderClient):
        self.recorderClients.remove(recorderClient)

    class recorderClient(threading.Thread):
        def __init__():
            # toggle to true on beat, false when client got the value
            self.onBeat = False
            # when registering the client i want to be able to define how long the avg list should be
            self.y_max_freq_avg_list = []
