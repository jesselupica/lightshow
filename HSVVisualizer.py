from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
import colorsys
import random

State = namedtuple('State', ['spectrum', 'is_hit', 'local_maxima', 'max_val', 'avg_amp'])

class HSVVisualizer(Visualizer):

    COLOR_TABLE = {'BLUE': float(2)/3, 'RED': 1, 'GREEN': float(1)/3}
    
    HISTORY_SIZE = 50
    HISTORY_SAMPLE = 10
    TREBLE_BASS_DIVIDE = 47
    
    def __init__(self, r, g, b):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        self.state_deque = deque([], maxlen=HSVVisualizer.HISTORY_SIZE)
        self.hue_chaser = 0
        
        self.bass_value_chaser = 0
        self.treble_value_chaser = 0
        
        self.bass_value_max = 0.5
        self.bass_value_min = 0.5

        self.treble_value_max = 0.5
        self.treble_value_min = 0.5

        self.bass_treble_ratio = 0.5

        self.visualize_music = True
        self.static_color = 'BLUE'
        
    def tuple(self):
        rgb = tuple( x * Visualizer.RGB_INTENSITY_MAX for x in colorsys.hsv_to_rgb(self.hue, self.saturation, self.value))
        return rgb

    def set_color(self, color):
        if color == 'BLACK':
            self.value = 0
            return

        self.saturation = 1
        self.value = 1
        self.hue = HSVVisualizer.COLOR_TABLE[color]
    
    def update_bass_treble_ratio(self, increase):
        incr = 0.05
        if increase:
            self.bass_treble_ratio += incr
        else:
            self.bass_treble_ratio -= incr
        self.bass_treble_ratio = min(1, self.bass_treble_ratio)
    
    def toggle_music_visualization(self):
        self.visualize_music = not self.visualize_music
        if not self.visualize_music:
            self.set_color(self.static_color)
    
    def visualize(self, raw_data, rate):
        if self.visualize_music:
            freqs = []
            
            for i in range(1, 88):
                # Taken from wikipedia for calculating frequency of each note on 88 key piano
                freqs.append(2**((i-49)/12) * 440)
            
            amps = self._get_amplitude_at_frequency(freqs, raw_data, rate)
            is_hit, local_maxima = self._update_colors(amps)

            index, value = max(enumerate(amps), key=lambda x: x[1])
            avg_amp = sum(amps)/len(amps)
        
            self.state_deque.append(State(amps, is_hit, local_maxima, index, avg_amp))
        
    def _bounds_check(self):
        self.hue = self.hue + 1 if self.hue < 0 else self.hue 
        self.saturation = min(self.saturation, 1)
        self.value = min(self.value, 1)

        self.hue = self.hue - 1 if self.hue > 1 else self.hue
        self.saturation = max(self.saturation, 0)
        self.value = max(self.value, 0)
        
    def _find_local_maxes(self, lst,max_threshold=0):
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

    def _is_hit(self, freq_amps, local_maxima, hit_coeff):
        sd = list(self.state_deque)[-1 * HSVVisualizer.HISTORY_SAMPLE:]

        if len(sd) >= 1: 
            for i in local_maxima:
               avg = sum((d.spectrum[i] for d in sd))/len(sd)
               if freq_amps[i] > hit_coeff * avg:
                   return True
        return False

    def _num_hits_in_hist(self, val=False):
        count = 0
        sd = list(self.state_deque)[-1 * HSVVisualizer.HISTORY_SAMPLE:]
        
        for state in sd:
            if (state.val_hit and val) or (state.is_hit and not val):
                count += 1
        return count
    
    def _avg_last_n_states(self, n, amp_size):
        sd = list(self.state_deque)[(-1 * n):]
        summed_amps = [0] * amp_size 
        for state in sd:
            for i, x in enumerate(state.spectrum):
                summed_amps[i] += x
        return [x/len(sd) for x in summed_amps]

    def _update_value_min_and_max(self, bass_pull_amount, treble_pull_amount):
        self.bass_value_max = max(self.bass_value_max, self.bass_value_chaser)
        self.base_value_min = min(self.bass_value_min, self.bass_value_chaser)
        self.bass_value_max -= bass_pull_amount
        self.bass_value_min += bass_pull_amount

        self.treble_value_max = max(self.treble_value_max, self.treble_value_chaser)
        self.base_value_min = min(self.treble_value_min, self.treble_value_chaser)
        self.treble_value_max -= treble_pull_amount
        self.treble_value_min += treble_pull_amount
    
    def _update_colors(self, freq_amps):
        hue_avgamount = 40
        hue_scale = 0.035

        bass_value_avgamount = 10
        bass_value_pull = 0.05

        treble_value_avgamount = 10
        treble_value_pull = 0.05

        local_maxima = self._find_local_maxes(freq_amps)

        is_hit = self._is_hit(freq_amps, local_maxima, 6)
        if is_hit:
            shift = (0.2 *(1/ (1+ self._num_hits_in_hist()))) 
            self.bass_value_chaser += shift
            self.treble_value_chaser += shift
            self.hue_chaser += shift
        
        if len(self.state_deque) > 5:
            avg_amps = self._avg_last_n_states(5, len(freq_amps))
            avg_max = max(enumerate(avg_amps), key=lambda x: x[1])[0]
        
            # Code for hue pusher taken from Sitar Harel and his LEDControl program
            h_chaser_diff = (avg_max - self.hue_chaser) / hue_avgamount

            self.hue_chaser += h_chaser_diff
            self.hue = self.hue + h_chaser_diff * hue_scale

        bass = freq_amps[:HSVVisualizer.TREBLE_BASS_DIVIDE]
        treble = freq_amps[HSVVisualizer.TREBLE_BASS_DIVIDE:]

        bass_mean_amp = sum(bass)/len(bass)
        treble_mean_amp = sum(treble)/len(treble)

        bass_v_chaser_diff = (bass_mean_amp - self.bass_value_chaser) / bass_value_avgamount
        treble_v_chaser_diff = (treble_mean_amp - self.treble_value_chaser) / treble_value_avgamount

        self.bass_value_chaser += bass_v_chaser_diff
        self.treble_value_chaser += treble_v_chaser_diff
        self._update_value_min_and_max(bass_value_pull, treble_value_pull)
        bass_val = (self.bass_value_chaser - self.bass_value_min)/ (self.bass_value_max - self.bass_value_min)
        treble_val = (self.treble_value_chaser - self.treble_value_min)/ (self.treble_value_max - self.treble_value_min)
        self.value = bass_val * self.bass_treble_ratio + treble_val * (1 - self.bass_treble_ratio)

        self._bounds_check()
        return is_hit, local_maxima
    
