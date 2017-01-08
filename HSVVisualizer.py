from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
import colorsys

State = namedtuple('State', ['spectrum', 'is_hit', 'local_maxima', 'max_val'])

class HSVVisualizer(Visualizer):
    
    HISTORY_SIZE = 10
    
    def __init__(self, r, g, b):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        self.state_deque = deque([], maxlen=HSVVisualizer.HISTORY_SIZE)

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

        index, value = max(enumerate(amps), key=operator.itemgetter(1))
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
        hit_coeff = 8.0

        if len(self.state_deque) >= 1: 
            for i in local_maxima:
               avg = sum((d.spectrum[i] for d in self.state_deque))/len(self.state_deque)
               if freq_amps[i] > hit_coeff * avg:
                   print(local_maxima)
                   return True
        return False

    def _num_hits_in_hist(self):
        count = 0
        for state in self.state_deque:
            if state.is_hit:
                count += 1
        return count
    
    def _update_colors(self, freq_amps):
        avgamount = 50

        local_maxima = self._find_local_maxes(freq_amps)

        #is_hit = self._is_hit(freq_amps, local_maxima)
        #if is_hit:
        #    shift = (0.2 - .02 * self._num_hits_in_hist()) 
        #    self.value += shift
        #    self.hue += shift

        is_hit = False
        
        print(sample_mean)
        # Code for hue pusher taken from Sitar Harel and his LEDControl program
        self.hue = self.hue + (sample_mean - self.hue) * (1.0/avgamount);
        #self.value -= 0.01
        self._bounds_check()
        return is_hit, local_maxima
