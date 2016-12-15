from sys import byteorder
import sys
from array import array
from struct import pack
from scipy.io import wavfile
import time
import math
import numpy
import pyaudio
import wave
import pygame
import random
from visualizer import ColorVisualizer

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

class Recording:
    def __init__(self, playback=True, file_name=None):
        p = pyaudio.PyAudio()
        self.playback = playback
        self.file_name = file_name
        if file_name:
            self.stream = wave.open(file_name, 'rb')
        else:
            self.stream = p.open(format=FORMAT, channels=1, rate=RATE,
                                input=True, output=True,
                                frames_per_buffer=CHUNK_SIZE)
        if playback:
            self.r_stream = p.open(format=p.get_format_from_width(self.stream.getsampwidth()),
                channels=self.stream.getnchannels(),
                rate=self.stream.getframerate(),
                output=True)
        self.is_over = False

    def get_chunk(self):
        try:
            if self.file_name:
                sound_data = array('h', self.stream.readframes(CHUNK_SIZE))
            else: 
                sound_data = array('h', self.stream.read(CHUNK_SIZE))
                if byteorder == 'big':
                    sound_data.byteswap()
            if self.playback: 
                self.r_stream.write(sound_data.tobytes())
            return sound_data
        except:
            self.is_over = True
            return None

    def still_playing(self):
        return not self.is_over

def get_amplitude_at_frequency(freqs, aud_data, samp_freq):
    s1 = numpy.array(aud_data)
    n = len(s1) 
    p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

    magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
    return [ magnitude[int(freq * n / samp_freq)] for freq in freqs ]

def get_dominant_frequency(samp_freq, aud_data):
    s1 = numpy.array(aud_data)
    n = len(s1) 
    p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

    magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
    max_mag = -float('inf')
    max_index = -1
    for i, x in enumerate(magnitude):
        if x > max_mag:
            max_mag= x
            max_index = i

    return max_index * samp_freq / n

def visualize(screen, file_name=None):
    # Start out white
    light_color = ColorVisualizer(255, 255, 255)
    music = Recording(file_name=file_name, playback=True if file_name else False)
    while music.still_playing(): 
        sound_data = music.get_chunk()
        if not sound_data:
            break

        freqs = []
        for i in range(1, 88):
            # Taken from wikipedia for calculating frequency of each note on 88 key piano
            freqs.append(2**((i-49)/12) * 440)
        #print(freqs)

        amps = get_amplitude_at_frequency(freqs, sound_data, RATE)
        #print(amps)
        #print([int(m) for m in max_intensities])
        light_color.update_colors(amps)
        screen.fill(light_color.tuple())
        pygame.display.flip()    

if __name__ == '__main__':
    (width, height) = (300, 200)
    background_colour = (0,255,0)
    black_color = 0,0,0

    print("Start recording...")

    screen = pygame.display.set_mode((width, height))
    screen.fill(black_color)
    pygame.display.flip()
    if len(sys.argv) >= 2:
        visualize(screen, file_name=sys.argv[1])
    else:
        visualize(screen)
    print("done")
