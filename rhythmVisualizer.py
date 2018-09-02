from __future__ import division
from visualizer import Visualizer
from collections import deque, namedtuple
import colorsys
import random
import numpy as np
import scipy.fftpack 
from scipy.signal import argrelextrema
import math
import time
from stream import Stream
from colors import NaiveHueSelector
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
delay = 0.42857


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
        self.energy_history = deque([], maxlen=max_len)
        self.sleep_history = deque([], maxlen=5*max_len)
        self.curr_intensity = 0
        self.last_hit = time.time()
        self.is_hit = None
        self.hit_mag = None

    def analyze(self, block):
        rl_sum = 0 
        for r, l in zip(block[::2], block[1::2]):
            rl_sum += abs(r) + abs(l)
        self.energy_history.append(rl_sum)
        self.sleep_history.append(rl_sum)
        self.curr_intensity = rl_sum

        avg = sum(self.energy_history)/len(self.energy_history)
        # var = np.var(np.array(self.energy_history))
        time_since_last_hit = time.time() - self.last_hit
        rest_interval_complete = time_since_last_hit > delay
        is_loud = self.curr_intensity > MIN_HIT_MULTIPLIER * avg
        self.is_hit = is_loud and rest_interval_complete

        if self.is_hit:
            self.last_hit = time.time()
            self.hit_mag = self.curr_intensity / avg

    def num_hits_in_hist(self, val=False):
        count = 110
        return count

    def get_intensity(self):
        max_intensity = max(self.energy_history)
        return self.curr_intensity / max_intensity

    def should_sleep(self):
        return max(self.sleep_history) < SLEEP_MAX


class RhythmVisualizer(Visualizer):

    TREBLE_BASS_DIVIDE = 30
    
    def __init__(self, r, g, b, stream=None):
        self.hue = 1
        self.saturation = 1
        self.value = 1
        
        self.stream = stream
        if not stream is None:
            self.stream_analyzer = StreamAnalyzer(HISTORY_DURATION, stream.RATE, stream.CHUNK_SIZE)
        
        self.desired_hue = 0
        self.hue_selector = NaiveHueSelector()
        
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
            if self.mode in (LightModes.VisualizeMusic, LightModes.Asleep):
                raw_data = self.stream.get_chunk()
                if not raw_data:
                    continue
                
                self.stream_analyzer.analyze(raw_data)
                if self.stream_analyzer.should_sleep():
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
        diff = self.desired_hue - self.hue
        if abs(diff) > 0.5:
            diff = -1 * np.sign(diff) * (1 - abs(diff))
        #print diff, self.desired_hue, self.hue, self.stream_analyzer.hit_mag
        self.hue += diff * HUE_CHASER_MULTIPLIER

        if self.stream_analyzer.is_hit:
            mag = self.stream_analyzer.hit_mag
            self.desired_hue = self.hue_selector.next(mag)
            shift = 0.2
            self.value_chaser += shift

        # bounds check
        self.desired_hue %= 1.0

        intensity = self.stream_analyzer.get_intensity()
        value_chaser_diff = (intensity - self.value_chaser) / VALUE_AVG_AMOUNT

        max_fall_rate = val_for_chunk(MAX_VALUE_FALL_SPEED_S, self.stream_analyzer.stream_chunk_size, self.stream_analyzer.stream_rate)
        self.value_chaser += value_chaser_diff
        pull = val_for_chunk(VALUE_PULL_RATE_S, self.stream_analyzer.stream_chunk_size, self.stream_analyzer.stream_rate)
        self.update_value_min_and_max(pull)
        self.value = (self.value_chaser - self.value_min)/ (self.value_max - self.value_min)
        self._bounds_check()
    
