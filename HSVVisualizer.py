from __future__ import division
from visualizer import Visualizer
from collections import deque
import colorsys

class HSVVisualizer(Visualizer):
    
    HISTORY_SIZE = 5

    def __init__(self, r, g, b):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        self.spectrum_deque = deque([], maxlen=HSVVisualizer.HISTORY_SIZE)

    def tuple(self):
        return tuple( x * Visualizer.RGB_INTENSITY_MAX for x in colorsys.hsv_to_rgb(self.hue, self.saturation, self.value))

    def visualize(self, raw_data, rate):
        freqs = []
        for i in range(1, 88):
            # Taken from wikipedia for calculating frequency of each note on 88 key piano
            freqs.append(2**((i-49)/12) * 440)

        amps = self._get_amplitude_at_frequency(freqs, raw_data, rate)
        self._update_colors(amps)

    def _find_local_maxes(self, lst):
        max_threshold = 0.3
        max_val = max(lst)
        max_indices = []
        incr = True
        for i, (e1, e2) in enumerate(zip(lst, lst[1:])):
            if incr and e1 > e2 and e1 > max_threshold * max_val:
                max_indices.append(i)
            # make sure we're not keeping track of marginal increases
            if e2 > e1 + 1:
                incr = True
            else: 
                incr = False
        return max_indices

    def _is_hit(self, freq_amps):

        hit_coeff = 3.5

        local_maxima = self._find_local_maxes(freq_amps)
        if len(self.spectrum_deque >= 1): 
            for i in local_maxima:
               avg = sum((d[i] for d in self.spectrum_deque))/len(self.spectrum_deque)
                if freq_amps[i] > hit_coeff * avg:
                    return True
        return False

    def _update_colors(self, freq_amps):
        is_hit = self._is_hit(freq_amps)
        if is_hit:
            self.value += 0.2

        self.value -= 0.035

        
