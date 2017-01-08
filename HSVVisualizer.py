from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
import colorsys
import random

State = namedtuple('State', ['spectrum', 'is_hit', 'local_maxima', 'max_val'])

class HSVVisualizer(Visualizer):
    
    HISTORY_SIZE = 50
    HISTORY_SAMPLE = 10
    def __init__(self, r, g, b):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        self.state_deque = deque([], maxlen=HSVVisualizer.HISTORY_SIZE)
        self.hue_chaser = 0
        
    def tuple(self):
        rgb = tuple( x * Visualizer.RGB_INTENSITY_MAX for x in colorsys.hsv_to_rgb(self.hue, self.saturation, self.value))
        return rgb

        
    def visualize(self, raw_data, rate):
        freqs = []
        for i in range(1, 88):
            # Taken from wikipedia for calculating frequency of each note on 88 key piano
            freqs.append(2**((i-49)/12) * 440)

        amps = self._get_amplitude_at_frequency(freqs, raw_data, rate)
        is_hit, local_maxima = self._update_colors(amps)

        index, value = max(enumerate(amps), key=lambda x: x[1])
        self.state_deque.append(State(amps, is_hit, local_maxima, index))
        
    def _bounds_check(self):
        self.hue = self.hue + 1 if self.hue < 0 else self.hue 
        self.saturation = min(self.saturation, 1)
        self.value = min(self.value, 1)

        self.hue = self.hue - 1 if self.hue > 1 else self.hue
        self.saturation = max(self.saturation, 0)
        self.value = max(self.value, 0)
        
    def _find_local_maxes(self, lst):
        max_threshold = 0.0
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

    def _is_hit(self, freq_amps, local_maxima):
        hit_coeff = 10.0
        sd = list(self.state_deque)[-1 * HSVVisualizer.HISTORY_SAMPLE:]

        if len(sd) >= 1: 
            for i in local_maxima:
               avg = sum((d.spectrum[i] for d in sd))/len(sd)
               if freq_amps[i] > hit_coeff * avg:
                   print(local_maxima)
                   return True
        return False

    def _num_hits_in_hist(self):
        count = 0
        sd = list(self.state_deque)[-1 * HSVVisualizer.HISTORY_SAMPLE:]
        
        for state in sd:
            if state.is_hit:
                count += 1
        return count

    def _update_colors(self, freq_amps):
        hue_avgamount = 40
        hue_scale = 0.035

        local_maxima = self._find_local_maxes(freq_amps)

        is_hit = self._is_hit(freq_amps, local_maxima)
        if is_hit:
            shift = random.choice([-1, 1]) * (0.2 *(1/ (1+ self._num_hits_in_hist()))) 
            self.value += shift
            self.hue += shift
            

        if len(self.state_deque) > 5:
            sd = list(self.state_deque)[-5:]
            avg = [0] * len(freq_amps) 
            for state in sd:
                for i, x in enumerate(state.spectrum):
                    avg[i] += x
            avg_max, av_max_val = max(enumerate(x/len(sd) for x in avg), key=lambda x: x[1])
        
            # Code for hue pusher taken from Sitar Harel and his LEDControl program
            chaser_diff = (avg_max - self.hue_chaser) / hue_avgamount

            self.hue_chaser += chaser_diff
            self.hue = self.hue + chaser_diff * hue_scale
        
        self._bounds_check()
        return is_hit, local_maxima
