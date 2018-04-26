from __future__ import division
from collections import deque
from visualizer import Visualizer
import time
import random
import numpy
import math

### Depreciated ###

class RGBVisualizer(Visualizer): 
    ACCELERATION = 12.5
    INIT_RGB_COEFF = 20, 20, 16
    GRAVITY = -8 #-6
    RGB_INTENSITY_MAX = 255
    RGB_INTENSITY_MIN = 0
    RGB_INTENSITY_THRESHOLD = 200
    RGB_COEFF_INCR = 1.02
    SIGNAL_INTENSITY_MAX_START = 300
    SIGNAL_INTENSITY_THRESHOLD = 1800
    
    SIGNAL_INTENSITY_DRAG = 5
    SIGNAL_INTENSITY_GAIN = 30

    HIT_CONST = 90
    HIT_COEFF = 3.5 #3

    BASELINE_FADE_MAX = 15
    BASELINE_FADE_STEP = 0.1
    
    def __init__(self, r, g, b, update_freq):
        r, g, b = self.rgb_bounds_check(r, g, b)
        self.red    = r if r > 1 else r * RGBVisualizer.RGB_INTENSITY_MAX
        self.green  = g if g > 1 else g * RGBVisualizer.RGB_INTENSITY_MAX
        self.blue   = b if b > 1 else b * RGBVisualizer.RGB_INTENSITY_MAX
        
        self.update_freq = update_freq
        # 5 is a magic number. I know. Get over it.
        self.signal_history = deque(maxlen=5)   
        self.sig_time_history = deque([time.time()], maxlen=5)

        # 3 for RGB 
        self.signal_intensity_maxes = [RGBVisualizer.SIGNAL_INTENSITY_MAX_START] * 3

        self.rgb_history = [deque([0], maxlen=50)] * 3
        self.rgb_max_mults = [1] * 3    

        self.rgb_raw_signal_history = [deque([0], maxlen=5)] * 3

        self.baseline_r = RGBVisualizer.BASELINE_FADE_MAX
        self.baseline_g = 0
        self.baseline_b = 0

    def _smooth(self, r, g, b):
        self.signal_history.append((r,g,b))
        r_sum, g_sum, b_sum = 0, 0, 0
        for ri, gi, bi in self.signal_history:
            r_sum += ri
            g_sum += gi
            b_sum += bi
        l = len(self.signal_history)
        return r_sum/l, g_sum/l, b_sum/l

    def _choose_rgb_signals(self, freq_amps):
        # 3 for RGB
        assert(len(freq_amps) >= 3)
        freq_amp_pairs = list(enumerate(freq_amps))
        sorted_fa_pairs = sorted(freq_amp_pairs, key=lambda x: x[1])
        rgb = sorted(sorted_fa_pairs[-3:], key=lambda x: x[0])
        return [x[1] for x in rgb], [x[0] for x in rgb]

    def _update_signal_intensity_multipliers(self):
        avg_rgb = [sum(d)/len(d) for d in self.rgb_history]
        for i, avg_c in enumerate(avg_rgb):
            if avg_c > RGBVisualizer.RGB_INTENSITY_THRESHOLD:
                self.rgb_max_mults[i] *= RGBVisualizer.RGB_COEFF_INCR
            elif self.rgb_max_mults[i] > 1:
                self.rgb_max_mults[i] /= RGBVisualizer.RGB_COEFF_INCR 

    def _is_hit(self, rgb_raw):
        avg_signal_amp = [sum(d)/len(d) for d in self.rgb_raw_signal_history]
        for sig, deq in zip(rgb_raw, self.rgb_raw_signal_history):
            deq.append(sig) 
        return [sig > RGBVisualizer.HIT_COEFF * avg for sig, avg in zip(rgb_raw, avg_signal_amp)]

    def _get_amplitude_at_frequency(self, freqs, aud_data, samp_freq):
        s1 = numpy.array(aud_data)
        n = len(s1) 
        p = numpy.fft.fft(s1) / float(n) # take the fourier transform 

        magnitude = [math.sqrt(x.real**2 + x.imag**2) for x in p]
        return [ magnitude[int(freq * n / samp_freq)] for freq in freqs ]

    def visualize(self, raw_data, rate):
        freqs = []
        for i in range(1, 88):
            # Taken from wikipedia for calculating frequency of each note on 88 key piano
            freqs.append(2**((i-49)/12) * 440)

        amps = self._get_amplitude_at_frequency(freqs, raw_data, rate)
        self._update_colors(amps)

    def _baseline_fade(self):
        # to make it easier to read
        bl = RGBVisualizer.BASELINE_FADE_MAX
        step = RGBVisualizer.BASELINE_FADE_STEP
        if self.baseline_r == bl and self.baseline_b == 0 and self.baseline_g < bl:
            self.baseline_g += step
            self.baseline_g = min(self.baseline_g, bl)
   
        elif self.baseline_g == bl and self.baseline_b == 0 and self.baseline_r > 0:
            self.baseline_r -= step
            self.baseline_r = max(0, self.baseline_r)

        elif self.baseline_r == 0 and self.baseline_g == bl and self.baseline_b < bl:
            self.baseline_b += step
            self.baseline_b = min(self.baseline_b, bl)
            
        elif self.baseline_r == 0 and self.baseline_b == bl and self.baseline_g > 0:
            self.baseline_g -= step
            self.baseline_g = max(0, self.baseline_g)

        elif self.baseline_g == 0 and self.baseline_b == bl and self.baseline_r < bl:
            self.baseline_r += step 
            self.baseline_r = min(self.baseline_r, bl)

        elif self.baseline_r == bl and self.baseline_g == 0 and self.baseline_b > 0:
            self.baseline_b -= step
            self.baseline_b = max(0, self.baseline_b)

        self.red = max(self.baseline_r, self.red)
        self.green = max(self.baseline_g, self.green)
        self.blue = max(self.baseline_b, self.blue)
            
    def _update_colors(self, freq_amps):

        self.sig_time_history.append(time.time())

        rgb_raw, _ = self._choose_rgb_signals(freq_amps)
        is_hit = self._is_hit(rgb_raw)
        if all(is_hit):
            # 7 in binary is 111, so I'm using this to determine boolean values for 3 ints
            bitwise_on = random.randint(1, 7)
            temp = [False] * 3
            if bitwise_on & 1 == 1:
                temp[0] = True
            if bitwise_on & 2 == 2:
                temp[1] = True 
            if bitwise_on & 4 == 4:
                temp[2] = True 
            is_hit = temp

        hit_const = [RGBVisualizer.HIT_CONST if h else 0 for h in is_hit]

        self._update_signal_intensity_multipliers()

        self.signal_intensity_maxes = [max(c,m) for c, m in zip(rgb_raw, self.signal_intensity_maxes)]
        r, g, b = [x/(m*mult) for x, m, mult in zip(rgb_raw, self.signal_intensity_maxes, self.rgb_max_mults)]
        smooth_r, smooth_g, smooth_b = self._smooth(r, g, b)

        excited_r = max(smooth_r, r)
        rv = RGBVisualizer.GRAVITY + RGBVisualizer.ACCELERATION * excited_r + hit_const[0]
        gv = RGBVisualizer.GRAVITY + RGBVisualizer.ACCELERATION * smooth_g  + hit_const[1]
        bv = RGBVisualizer.GRAVITY + RGBVisualizer.ACCELERATION * smooth_b  + hit_const[2]

        for i, m_i in enumerate(self.signal_intensity_maxes):
            if m_i > RGBVisualizer.SIGNAL_INTENSITY_DRAG:
                drag = RGBVisualizer.SIGNAL_INTENSITY_DRAG 
                if m_i > RGBVisualizer.SIGNAL_INTENSITY_THRESHOLD:
                    drag *= RGBVisualizer.INIT_RGB_COEFF[i]
                self.signal_intensity_maxes[i] = max(RGBVisualizer.SIGNAL_INTENSITY_MAX_START, m_i - drag)

        vels = [rv, gv,  bv]
        min_index = min(enumerate(vels), key=lambda x: x[1])[0] 

        vels[min_index] = RGBVisualizer.GRAVITY
        
        self.red += vels[0]
        self.green += vels[1]
        self.blue += vels[2]

        #print(min([(rv,1), (gv, 2), (bv, 3)], key=lambda x: x[0]))
        
        self._baseline_fade()
        
        self.red, self.green, self.blue = self.rgb_bounds_check(self.red, self.green, self.blue)
        rgb = [self.red, self.green, self.blue]
        for c, c_deque in zip(rgb, self.rgb_history):
            c_deque.append(c)

