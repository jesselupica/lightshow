from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
from itertools import cycle
import colorsys
import random
import numpy as np
import math
from stream import Stream

State = namedtuple('State', ['spectrum', 'is_hit', 'local_maxima', 'max_val', 'avg_amp'])

HUE_AVG_AMOUNT = 40
HUE_CHASER_MULTIPLIER = 0.01
HUE_SHIFT_MULTIPLIER = 2

VALUE_AVG_AMOUNT = 10
VALUE_PULL = 0.30 #0.4 is a good number

HISTORY_SIZE = 50
HISTORY_SAMPLE_SIZE = 20
HISTORY_DURATION = 2

FREQS = [4186.01, 3951.07, 3729.31, 3520.00, 3322.44, 3135.96, 2959.96,
  2793.83, 2637.02, 2489.02, 2349.32, 2217.46, 2093.00, 1975.53, 1864.66,
  1760.00, 1661.22, 1567.98, 1479.98, 1396.91, 1318.51, 1244.51, 1174.66, 
  1108.73, 1046.50, 987.767, 932.328, 880.000, 830.609, 783.991, 739.989, 
  698.456, 659.255, 622.254, 587.330, 554.365, 523.251, 493.883, 466.164, 
  440.000, 415.305, 391.995, 369.994, 349.228, 329.628, 311.127, 293.665, 
  277.183, 261.626, 246.942, 233.082, 220.000, 207.652, 195.998, 184.997, 
  174.614, 164.814, 155.563, 146.832, 138.591, 130.813, 123.471, 116.541, 
  110.000, 103.826, 97.9989, 92.4986, 87.3071, 82.4069, 77.7817, 73.4162, 
  69.2957, 65.4064, 61.7354, 58.2705, 55.0000, 51.9130, 48.9995, 46.2493, 
  43.6536, 41.2035, 38.8909, 36.7081, 34.6479, 32.7032, 30.8677, 29.1353, 
  27.5000]

# Enum
class LightModes:
    VisualizeMusic = 'VISUALIZE_MUSIC'
    StaticColor = 'STATIC_COLOR'
    Fade = 'FADE'
    Asleep = 'ASLEEP'
    Off = 'OFF'
    CustomStaticColor = 'CUSTOM_STATIC_COLOR'

class StreamAnalyzer:
    def __init__(self, history_duration_s, stream_rate, stream_chunk_size):
        self.stream_rate = stream_rate
        max_len = history_duration_s * stream_rate / stream_chunk_size
        self.state_history = deque([], maxlen=max_len)
        self.freq_amp_history = deque([], maxlen=max_len)

    def analyze(self, block):
        amps = self.get_amplitude_at_frequency(block)
        local_maxima = self.find_local_maxes(amps)
        is_hit = self.is_hit(amps, local_maxima, 6)

    def get_amplitude_at_frequency(self, aud_data, freqs=FREQS):
        s1 = np.array(aud_data)
        n = s1.size
        p = np.fft.fft(s1) / float(n) # take the fourier transform 

        magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
        return [ magnitude[int(freq * n / self.stream_rate)] for freq in freqs ]

    def num_hits_in_hist(self, val=False):
        count = 0
        sd = list(self.state_history)[-1 * HISTORY_SAMPLE_SIZE:]
        
        for state in sd:
            if state.is_hit and not val:
                count += 1
        return count

    def find_local_maxes(self, lst, max_threshold=0):
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

    def is_hit(self, freq_amps, local_maxima, hit_coeff):
        sd = list(self.state_history)[-1 * HISTORY_SAMPLE_SIZE:]

        if len(sd) >= 1: 
            for i in local_maxima:
               avg = sum((d.spectrum[i] for d in sd))/len(sd)
               if freq_amps[i] > hit_coeff * avg:
                   return True
        return False

class HSVVisualizer(Visualizer):
    color_table = {'RED': 1, 'ORANGE':0.038888, 'GREEN': 0.3333, 'TEAL':0.5527777, 'BLUE': 0.66666, 'PURPLE': 0.783333, 'PINK':0.9444  }

    TREBLE_BASS_DIVIDE = 30
    
    def __init__(self, r, g, b, stream=None):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        
        self.stream = stream
        if not stream is None:
            self.stream_analyzer = StreamAnalyzer(HISTORY_DURATION, stream.RATE, stream.CHUNK_SIZE)
        
        self.hue_chaser = 0
        self.hues = cycle(sorted(HSVVisualizer.color_table.values()))
        
        self.value_chaser = 0.5
        self.value_max = 0.5
        self.value_min = 0.5

        self.mode = LightModes.VisualizeMusic
        self.static_color = 'BLUE'
        self.fade_speed = 0.001
        self.fade_speed_range = 0.0001, 0.01

        self.amps = []

    def attach_stream(self, stream):
        self.stream = stream
        self.stream_analyzer = StreamAnalyzer(HISTORY_DURATION, stream.RATE, stream.CHUNK_SIZE)

        
    def tuple(self):
        max_val = Visualizer.RGB_INTENSITY_MAX
        rgb_vals = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        return tuple( val * max_val for val in rgb_vals)

    def get_state(self):
        interface_fade_speed = (self.fade_speed - self.fade_speed_range[0]) / (self.fade_speed_range[1] - self.fade_speed_range[0]) 
        return {'hue': self.hue, 'saturation': self.saturation, 
                'value':self.value, 'mode': self.mode, 
                'is_asleep':self.mode == LightModes.Asleep, 'fade_speed' : interface_fade_speed}

    def turn_off_lights(self):
        self.set_color('BLACK')
        self.mode = LightModes.Off

    def turn_on_music_visualization(self):
        self.mode = LightModes.VisualizeMusic

    def turn_on_fade(self):
        self.mode = LightModes.Fade
        self.value = 1
        self.saturation = 1

    def set_hue(self, hue):
        self.mode = LightModes.CustomStaticColor
        self.hue = hue
        self._bounds_check()

    def set_sat(self, sat):
        self.saturation = sat
        self._bounds_check()

    def set_brightness(self, brightness):
        self.value = brightness
        self._bounds_check()

    # fade speed should be between 0 and 1 
    # where 1 is the max fade speed and 0 is the min fade speed
    # if you want to change those values, that's in the constructor
    def set_fade_speed(self, fade_speed):
        transformed_val = (self.fade_speed_range[1] - self.fade_speed_range[0]) * fade_speed + self.fade_speed_range[0]
        self.fade_speed = transformed_val

    def set_color(self, color):
        self.mode = LightModes.StaticColor

        self.static_color = color
        if color == 'BLACK':
            self.value = 0
            return

        old_sat = self.saturation
        old_val = self.value

        self.saturation = 1
        self.value = 1
        try:
            self.hue = HSVVisualizer.color_table[color]
        except: 
            self.saturation = old_sat
            self.value = old_val  
        self._bounds_check()

    def toggle_music_visualization(self):
        if self.mode == LightModes.VisualizeMusic:
            self.set_color(self.static_color)
        else:
            self.mode = LightModes.VisualizeMusic

    def visualize(self):
        while True:
            raw_data = self.stream.get_chunk()
            if self.mode in (LightModes.VisualizeMusic, LightModes.Asleep):
                if not raw_data:
                    continue
                self.stream_analyzer.analyze(raw_data)
                is_hit, local_maxima = self.update_color(self.amps)

                index, value = max(enumerate(self.amps), key=lambda x: x[1])
                avg_amp = sum(self.amps)/len(self.amps)
            
                self.state_deque.append(State(self.amps, is_hit, local_maxima, index, avg_amp))

            elif self.mode == LightModes.StaticColor:
                self.set_color(self.static_color)
            elif self.mode == LightModes.Fade:
                self.update_fade()

    def update_fade(self):
        self.hue += self.fade_speed
        self._bounds_check()

    def _bounds_check(self):
        self.hue %= 1.0
        self.saturation = min(self.saturation, 1)
        self.saturation = max(self.saturation, 0)
        self.value = min(self.value, 1)
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
        sd = list(self.state_deque)[-1 * HISTORY_SAMPLE_SIZE:]

        if len(sd) >= 1: 
            for i in local_maxima:
               avg = sum((d.spectrum[i] for d in sd))/len(sd)
               if freq_amps[i] > hit_coeff * avg:
                   return True
        return False

    def _num_hits_in_hist(self, val=False):
        count = 0
        sd = list(self.state_deque)[-1 * HISTORY_SAMPLE_SIZE:]
        
        for state in sd:
            if state.is_hit and not val:
                count += 1
        return count

    def update_value_min_and_max(self, pull_amount):
        self.value_max = max(self.value_max, self.value_chaser)
        self.value_min = min(self.value_min, self.value_chaser)
        self.value_max -= pull_amount
        self.value_min += pull_amount

        if self.value_max < 5:
            self.mode = LightModes.Asleep
        else: 
            self.mode = LightModes.VisualizeMusic
    
    def update_color(self, freq_amps):
        self.hue += (self.hue_chaser - self.hue) * HUE_CHASER_MULTIPLIER

        if self.stream_analyzer.is_hit():
            hits_in_history = self.stream_analyzer.num_hits_in_hist()
            if hits_in_history == 0:
                self.hue_chaser = next(self.hues)

            shift = 0.2 * (1 / (1 + hits_in_history))
            self.value_chaser += shift
            self.value_chaser += shift

        self.hue_chaser %= 1.0
        mean_amp = sum(freq_amps)/len(freq_amps)

        value_chaser_diff = (mean_amp - self.value_chaser) / VALUE_AVG_AMOUNT

        self.value_chaser += value_chaser_diff
        self.update_value_min_and_max(VALUE_PULL)
        self.value = (self.value_chaser - self.value_min)/ (self.value_max - self.value_min)
        self.rgb_bounds_check()
    
