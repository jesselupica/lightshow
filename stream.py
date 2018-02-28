from __future__ import division
from sys import byteorder
from array import array
import wave
import os
import traceback
import pyaudio
import numpy as np

class Stream(object):
    CHUNK_SIZE = 1024
    RATE = 44100
    def __init__(self):
        p = pyaudio.PyAudio()
        self.input_stream = p.open(format=pyaudio.paInt16, channels=1, rate=Stream.RATE,
                            input=True,
                            frames_per_buffer=Stream.CHUNK_SIZE)

    def get_chunk(self):
        try:
            sound_data = array('h', self.input_stream.read(Stream.CHUNK_SIZE, exception_on_overflow = False))
            if byteorder == 'big':
              	 sound_data.byteswap()
            return sound_data
        except IOError as e:
            print e
            return None
	    
    def spec(self):
        return Stream.CHUNK_SIZE, Stream.RATE 

class FileStream(Stream):
    def __init__(self, file_name):
        p = pyaudio.PyAudio()
        self.wf = wave.open(file_name, mode='rb')
        self.output_stream = p.open(format =
                p.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True) 
        #data = self.wf.readframes(130000)


    def get_chunk(self):
        try:
            data = self.wf.readframes(1024)
            sound_data = array('h', data)
            # data = self.wf.readframes(Stream.CHUNK_SIZE)
            # sig = np.frombuffer(data, dtype='<i2').reshape(-1, self.wf.getnchannels())
            # sound_data = sig.transpose
            self.output_stream.write(data)
            return sound_data
        except IOError as e:
           return None


