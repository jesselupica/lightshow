from __future__ import division
from sys import byteorder
from array import array
import wave
import os
import traceback
import pyaudio

class Recording:

    CHUNK_SIZE = 512
    RATE = 44100

    def __init__(self, playback=False, file_name=None):

        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=Recording.RATE,
                                 input=True,
                                frames_per_buffer=Recording.CHUNK_SIZE)
        if playback:
            self.r_stream = p.open(format=pyaudio.paInt16, channels=2, rate=Recording.RATE,
                                 output=True,
                                frames_per_buffer=Recording.CHUNK_SIZE) 
        self.is_over = False
        self.playback = playback
        self.file_name = file_name
        
    def get_chunk(self):
        try:
            if self.file_name:
                sound_data = array('h', self.stream.readframes(Recording.CHUNK_SIZE))
            else:
                sound_data = array('h', self.stream.read(Recording.CHUNK_SIZE))
                if byteorder == 'big':
              	    sound_data.byteswap()
            if self.playback: 
                self.r_stream.write(sound_data.tostring())
            return sound_data
        except IOError as e:
	    pass
	except Exception as e:
            traceback.print_exc()
            self.is_over = True
            return None

    def still_playing(self):
        return not self.is_over

    def spec(self):
        return Recording.CHUNK_SIZE, Recording.RATE 
