from collections import deque
import time

class ColorVisualizer: 
    # acc 10 gravity -4 works well

    # gooey
    # ACCELERATION = 10
    # G_CONST = 2
    # B_CONST = 1
    # R_CONST = 4
    # GRAVITY = -4

    ACCELERATION = 12.5
    INIT_RGB_COEFF = 12, 20, 16
    GRAVITY = -6
    RGB_INTENSITY_MAX = 255
    RGB_INTENSITY_MIN = 0
    RGB_INTENSITY_THRESHOLD = 200
    RGB_COEFF_INCR = 1.02
    SIGNAL_INTENSITY_MAX_START = 300
    SIGNAL_INTENSITY_THRESHOLD = 1800
    
    SIGNAL_INTENSITY_DRAG = 5
    SIGNAL_INTENSITY_GAIN = 30

    def __init__(self, r, g, b):
        r, g, b = self._bounds_check(r, g, b)
        self.red    = r if r > 1 else r * ColorVisualizer.RGB_INTENSITY_MAX
        self.green  = g if g > 1 else g * ColorVisualizer.RGB_INTENSITY_MAX
        self.blue   = b if b > 1 else b * ColorVisualizer.RGB_INTENSITY_MAX

        self.rv = 0
        self.bv = 0
        self.gv = 0     
        # 5 is a magic number. I know. Get over it.
        self.signal_history = deque(maxlen=5)   
        self.sig_time_history = deque([time.time()], maxlen=5)

        # 3 for RGB 
        self.signal_intensity_maxes = [ColorVisualizer.SIGNAL_INTENSITY_MAX_START] * 3

        self.rgb_history = [deque([0], maxlen=50)] * 3
        self.rgb_max_mults = [1] * 3
    

    def tuple(self):
        #print(str(self.red) + ', ' + str(self.green) + ', ' + str(self.blue))
        return (self.red, self.green, self.blue)

    def _bounds_check(self, r, g, b):
        r = min(r, ColorVisualizer.RGB_INTENSITY_MAX)
        g = min(g, ColorVisualizer.RGB_INTENSITY_MAX)
        b = min(b, ColorVisualizer.RGB_INTENSITY_MAX)

        r = max(r, ColorVisualizer.RGB_INTENSITY_MIN)
        g = max(g, ColorVisualizer.RGB_INTENSITY_MIN)
        b = max(b, ColorVisualizer.RGB_INTENSITY_MIN)

        return r, g, b

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
        # for i, m_i in enumerate(max_intensities):
        #    if m_i > intensity_drag:
        #        max_intensities[i] = max(300, m_i - intensity_drag)
        # 3 for RGB
        assert(len(freq_amps) >= 3)
        freq_amp_pairs = list(enumerate(freq_amps))
        sorted_fa_pairs = sorted(freq_amp_pairs, key=lambda x: x[1])
        rgb = sorted(sorted_fa_pairs[-3:], key=lambda x: x[0])
        #print([ int(2**((i-49)/12) * 440) for i, a in rgb])
        return [x[1] for x in rgb]

    def _update_signal_intensity_multipliers(self):
        avg_rgb = [sum(d)/len(d) for d in self.rgb_history]
        #print(avg_rgb, len(self.rgb_history[0]))
        for i, avg_c in enumerate(avg_rgb):
            if avg_c > ColorVisualizer.RGB_INTENSITY_THRESHOLD:
                self.rgb_max_mults[i] *= ColorVisualizer.RGB_COEFF_INCR
            elif self.rgb_max_mults[i] > 1:
                self.rgb_max_mults[i] /= ColorVisualizer.RGB_COEFF_INCR 

    def update_colors(self, freq_amps):

        dt = time.time() - self.sig_time_history[-1]
        self.sig_time_history.append(time.time())

        rgb_raw = self._choose_rgb_signals(freq_amps)
        self._update_signal_intensity_multipliers()

        self.signal_intensity_maxes = [max(c,m) for c, m in zip(rgb_raw, self.signal_intensity_maxes)]
        r, g, b = [x/(m*mult) for x, m, mult in zip(rgb_raw, self.signal_intensity_maxes, self.rgb_max_mults)]
        smooth_r, smooth_g, smooth_b = self._smooth(r, g, b)
        #print(smooth_r, smooth_g, smooth_b)

        excited_r = max(smooth_r, r)
        self.rv = ColorVisualizer.GRAVITY + ColorVisualizer.ACCELERATION * excited_r 
        self.gv = ColorVisualizer.GRAVITY + ColorVisualizer.ACCELERATION * smooth_g 
        self.bv = ColorVisualizer.GRAVITY + ColorVisualizer.ACCELERATION * smooth_b 

       # print(self.rgb_coeff)

        for i, m_i in enumerate(self.signal_intensity_maxes):
            if m_i > ColorVisualizer.SIGNAL_INTENSITY_DRAG:
                drag = ColorVisualizer.SIGNAL_INTENSITY_DRAG 
                if m_i > ColorVisualizer.SIGNAL_INTENSITY_THRESHOLD:
                    drag *= ColorVisualizer.INIT_RGB_COEFF[i]
                self.signal_intensity_maxes[i] = max(ColorVisualizer.SIGNAL_INTENSITY_MAX_START, m_i - drag)

        self.red += self.rv 
        self.green += self.gv
        self.blue += self.bv

        self.red, self.green, self.blue = self._bounds_check(self.red, self.green, self.blue)
        rgb = [self.red, self.green, self.blue]
        for c, c_deque in zip(rgb, self.rgb_history):
            c_deque.append(c)

