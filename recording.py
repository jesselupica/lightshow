from __future__ import division
from sys import byteorder
from array import array
import pyaudio
import wave
import alsaaudio
import os

class Recording:

    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100

    def __init__(self, playback=True, file_name=None):

        uname = os.uname()
        if uname[0] == 'Linux':
            self.is_pi = True
            card = 'default'
            inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
            inp.setchannels(1)
            inp.setrate(Recording.RATE)
            inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            inp.setperiodsize(Recording.CHUNK_SIZE)
            self.stream = inp
        else:
            self.is_pi = False
            inp = pyaudio.PyAudio()
            if file_name:
                self.stream = wave.open(file_name, 'rb')
            else:
                self.stream = inp.open(format=Recording.FORMAT, channels=1, rate=Recording.RATE,
                                 input=True,
                                frames_per_buffer=Recording.CHUNK_SIZE)
            if playback:
                self.r_stream = self.stream 
        self.is_over = False
        self.playback = playback
        self.file_name = file_name
        
    def get_chunk(self):
        try:
            if self.is_pi:
                l, sound_bytes = self.stream.read()
                sound_data = array('h', sound_bytes)
            else:
                if self.file_name:
                    sound_data = array('h', self.stream.readframes(Recording.CHUNK_SIZE))
                else: 
                    sound_data = array('h', self.stream.read(Recording.CHUNK_SIZE))
                    if byteorder == 'big':
                        sound_data.byteswap()
            #if self.playback: 
            #    self.r_stream.write(sound_data.tobytes())
            return sound_data
        except:
            self.is_over = True
            return None

    def still_playing(self):
        return not self.is_over

    def spec(self):
        return Recording.CHUNK_SIZE, Recording.RATE 
