from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
from itertools import cycle
import colorsys
import random
import numpy as np
import scipy.fftpack 
from scipy.signal import argrelextrema
import math
from stream import Stream

State = namedtuple('State', ['spectrum', 'is_hit', 'intensity', 'raw_data'])

HUE_AVG_AMOUNT = 40
HUE_CHASER_MULTIPLIER = 0.01
HUE_SHIFT_MULTIPLIER = 2

VALUE_AVG_AMOUNT = 40
VALUE_PULL_RATE_S = 0.03

HISTORY_DURATION = 2

SLEEP_MAX = 3000

MAX_VALUE_FALL_SPEED_S = 2

MIN_HIT_MULTIPLIER = 1.5142857

MIN_BRIGHTNESS = 0 # out of 255

# frequencies for all 88 keys on a piano 
FREQS = [27.5, 29.1353, 30.8677, 32.7032, 34.6479, 36.7081, 38.8909, 41.2035, 43.6536, 46.2493, 48.9995, 51.913, 55.0, 58.2705, 61.7354, 65.4064, 69.29573,  73.4162, 77.7817, 82.4069, 87.3071, 92.4986, 97.9989, 103.826, 110.0, 116.541, 123.471, 130.813, 138.591, 146.832, 155.563, 164.814, 174.614, 184.997, 195.998, 207.652, 220.0, 233.082, 246.942, 261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440.0, 466.164, 493.883, 523.251, 554.365, 587.33, 622.254, 659.255, 698.456, 739.989, 783.991, 830.609, 880.0, 932.328, 987.767, 1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 1864.66, 1975.53, 2093.0, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.0, 3729.31, 3951.07, 4186.01]

def val_for_chunk(rate, chunk_size, stream_rate):
    return rate * chunk_size / stream_rate

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
        self.stream_chunk_size = stream_chunk_size
        max_len = history_duration_s * stream_rate / stream_chunk_size
        self.state_history = deque([], maxlen=max_len)
        self.raw_history = deque([], maxlen=max_len)
        self.energy_history = deque([], maxlen=max_len)
        self.curr_state = None
        self.sleep_history = deque([], maxlen=5*max_len)

    def analyze(self, block):
        amps, intensity = self.extract_data(block)
        local_maxima = np.transpose(argrelextrema(amps, np.greater))
        hit = self.is_hit(amps, local_maxima, MIN_HIT_MULTIPLIER)
        s = State(amps, hit, intensity, block)
        self.curr_state = s
        self.state_history.append(s)

    def extract_data(self, aud_data, freqs=FREQS):
        s1 = np.array(aud_data)
        magnitude = np.abs(scipy.fftpack.fft(s1)[:self.stream_chunk_size]) * 2 / (256 * self.stream_chunk_size)
        
        notes = []
        last_divder = 0
        for f1, f2 in zip(FREQS, FREQS[1:]):
            curr_divider = int(f1 + f2 / 2)
            note_range = magnitude[last_divder:curr_divider]
            if len(note_range) == 0:
                notes.append(0)
            else:
                max_val = max(note_range)
                avg_val = sum(note_range) / len(note_range)
                notes.append(max_val) # avg looks better than max
            last_divder = curr_divider

        rl_sum = 0 
        for r, l in zip(aud_data[::2], aud_data[1::2]):
            rl_sum += abs(r) + abs(l)
        self.energy_history.append(rl_sum)
        self.sleep_history.append(rl_sum)
        return np.array(notes), rl_sum

    def num_hits_in_hist(self, val=False):
        count = 0
        sd = list(self.state_history)
        
        for state in sd:
            if state.is_hit and not val:
                count += 1
        return count

    def is_hit(self, freq_amps, local_maxima, hit_coeff):
        if not self.curr_state:
            return False
        curr_intensity = self.curr_state.intensity
        avg = sum(self.energy_history)/len(self.energy_history)
        # var = np.var(np.array(self.energy_history))
        return curr_intensity > MIN_HIT_MULTIPLIER * avg

class RhythmVisualizer(Visualizer):
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
        self.hues = cycle(sorted(RhythmVisualizer.color_table.values()))
        
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
        rgb_vals = colorsys.hsv_to_rgb(self.hue, self.saturation, max(self.value, MIN_BRIGHTNESS / 255))
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
            self.hue = RhythmVisualizer.color_table[color]
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
                
                if max(self.stream_analyzer.sleep_history) < SLEEP_MAX:
                    self.mode = LightModes.Asleep
                else:
                    self.mode = LightModes.VisualizeMusic
                self.update_color()
                    
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

        if self.value_max - self.value_min < 0.003:
            self.mode = LightModes.Asleep
        else: 
            self.mode = LightModes.VisualizeMusic
    
    def update_color(self):
        if self.mode == LightModes.Asleep:
            self.value = 0
            return
        
        diff = self.hue_chaser - self.hue
        if abs(diff) > 0.5:
            diff = -1 * np.sign(diff) * (1 - abs(diff))

        self.hue += (self.hue_chaser - self.hue) * HUE_CHASER_MULTIPLIER
        hits_in_history = 0
        if self.stream_analyzer.curr_state.is_hit:
            hits_in_history = self.stream_analyzer.num_hits_in_hist()
            if hits_in_history < 10 :
                self.hue_chaser = next(self.hues)

            shift = 0.2 * (1 / (1 + hits_in_history))
            self.value_chaser += shift

        self.hue_chaser %= 1.0

        if self.stream_analyzer.curr_state:
            max_intensity = max(self.stream_analyzer.energy_history)
            intensity = self.stream_analyzer.curr_state.intensity / max_intensity
        else:
            intensity = 0 
        value_chaser_diff = (intensity - self.value_chaser) / VALUE_AVG_AMOUNT
        

        max_fall_rate = val_for_chunk(MAX_VALUE_FALL_SPEED_S, self.stream_analyzer.stream_chunk_size, self.stream_analyzer.stream_rate)
        self.value_chaser += value_chaser_diff
        pull = val_for_chunk(VALUE_PULL_RATE_S, self.stream_analyzer.stream_chunk_size, self.stream_analyzer.stream_rate)
        self.update_value_min_and_max(pull)
        self.value = (self.value_chaser - self.value_min)/ (self.value_max - self.value_min)
        self._bounds_check()
    
