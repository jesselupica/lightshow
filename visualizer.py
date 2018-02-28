from __future__ import division
import numpy
import math
from array import array

class Visualizer(object):

    RGB_INTENSITY_MAX = 255
    RGB_INTENSITY_MIN = 0

    def __init__(self, r, g, b):
        self.red    = r if r > 1 else r * Visualizer.RGB_INTENSITY_MAX
        self.green  = g if g > 1 else g * Visualizer.RGB_INTENSITY_MAX
        self.blue   = b if b > 1 else b * Visualizer.RGB_INTENSITY_MAX

    def tuple(self):
        return (self.red, self.green, self.blue)

    def _bounds_check(self, r, g, b):
        r = min(r, Visualizer.RGB_INTENSITY_MAX)
        g = min(g, Visualizer.RGB_INTENSITY_MAX)
        b = min(b, Visualizer.RGB_INTENSITY_MAX)

        r = max(r, Visualizer.RGB_INTENSITY_MIN)
        g = max(g, Visualizer.RGB_INTENSITY_MIN)
        b = max(b, Visualizer.RGB_INTENSITY_MIN)

        return r, g, b

    def _get_amplitude_at_frequency(self, freqs, aud_data, samp_freq):
        s1 = numpy.array(aud_data)
        n = s1.size
        p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

        magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
        return [ magnitude[int(freq * n / samp_freq)] for freq in freqs ]

    def visualize(self, raw_data, rate):
        raise NotImplementedError

