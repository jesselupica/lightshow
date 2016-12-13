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

sampFreq, snd = wavfile.read('440_sine.wav')


THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

class Color: 

    ACCELERATION = 10
    GRAVITY = -4
    MAX_INTENSITY = 255
    MIN_INTENSITY = 0
    def __init__(self, r, g, b):
        r, g, b = self._bounds_check(r, g, b)
        self.red = r if r > 1 else r * Color.MAX_INTENSITY
        self.green = g if g < 1 else g * Color.MAX_INTENSITY
        self.blue = b if b < 1 else b * Color.MAX_INTENSITY

        self.rv = 0
        self.bv = 0
        self.gv = 0
        self.time = time.time()

    def tuple(self):
        print((self.red, self.blue, self.green))
        return (self.red, self.blue, self.green)

    def _bounds_check(self, r, g, b):
        r = min(r, Color.MAX_INTENSITY)
        g = min(g, Color.MAX_INTENSITY)
        b = min(b, Color.MAX_INTENSITY)

        r = max(r, Color.MIN_INTENSITY)
        g = max(g, Color.MIN_INTENSITY)
        b = max(b, Color.MIN_INTENSITY)

        return r, g, b

    def update_colors(self, r, g, b):
        self.rv = Color.GRAVITY + Color.ACCELERATION * r / Color.MAX_INTENSITY
        self.gv = Color.GRAVITY + Color.ACCELERATION * g / Color.MAX_INTENSITY
        self.bv = Color.GRAVITY + Color.ACCELERATION * b / Color.MAX_INTENSITY

        self.red += self.rv 
        self.green += self.gv
        self.blue += self.bv

        self.red, self.green, self.blue = self._bounds_check(self.red, self.green, self.blue)


def get_amplitude_at_frequency(freq, aud_data, samp_freq):
    #samp_freq, snd = wavfile.read('440_sine.wav')
    #s1 = snd[:,0]
    #s2 = snd[:,1]
    s1 = numpy.array(aud_data)
    n = len(s1) 
    p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

    magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
    index = int(int(freq) * n / int(samp_freq))

    return magnitude[index]

def get_dominant_frequency(samp_freq, aud_data):
    #samp_freq, snd = wavfile.read('440_sine.wav')
    #s1 = snd[:,0]
    #s2 = snd[:,1]
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

def record(screen):
    p = pyaudio.PyAudio()
    playback = False
    if len(sys.argv) >= 2:
        print("opening song: " + str(sys.argv))
        stream = wave.open(sys.argv[1], 'rb')
        playback = True
    else: 
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK_SIZE)

    r_stream = p.open(format=p.get_format_from_width(stream.getsampwidth()),
                channels=stream.getnchannels(),
                rate=stream.getframerate(),
                output=True)
    max_reasonable_amp = 200
    max_intensity_seen = 0

    light_color = Color(255, 255, 255)
    while True:
        # little endian, signed short
        if playback: 
            sound_data = stream.readframes(CHUNK_SIZE)
            r_stream.write(sound_data.tobytes())
        else:
            sound_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                sound_data.byteswap()
        
        freq = get_dominant_frequency(RATE, sound_data)
        dom_amp = get_amplitude_at_frequency(440, sound_data, RATE)
        dom_amp = max(dom_amp, 1)

        if dom_amp < max_reasonable_amp:
            max_intensity_seen = max(dom_amp, max_intensity_seen)
        else: 
            dom_amp = max_intensity_seen
        blue = get_amplitude_at_frequency(440, sound_data, RATE) #/ max_intensity_seen
        green = get_amplitude_at_frequency(250, sound_data, RATE) #/ max_intensity_seen
        red = get_amplitude_at_frequency(100, sound_data, RATE) #/ max_intensity_seen

        light_color.update_colors(red, green, blue)
        screen.fill(light_color.tuple())
        pygame.display.flip()
        
    stream.stop_stream()
    stream.close()
    p.terminate()
    

if __name__ == '__main__':
    (width, height) = (300, 200)
    background_colour = (255,255,255)
    black_color = 0,0,0

    print("Start recording...")

    screen = pygame.display.set_mode((width, height))
    screen.fill(black_color)
    pygame.display.flip()

    record(screen)
    print("done")
