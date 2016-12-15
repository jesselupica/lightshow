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
    RGB_CONST = 12, 20, 16
    GRAVITY = -6
    MAX_INTENSITY = 255
    MIN_INTENSITY = 0
    SIGNAL_INTENSITY_MAX_START = 300
    SIGNAL_INTENSITY_THRESHOLD = 1800
    
    SIGNAL_INTENSITY_DRAG = 5
    SIGNAL_INTENSITY_GAIN = 30

    def __init__(self, r, g, b):
        r, g, b = self._bounds_check(r, g, b)
        self.red = r if r > 1 else r * ColorVisualizer.MAX_INTENSITY
        self.green = g if g < 1 else g * ColorVisualizer.MAX_INTENSITY
        self.blue = b if b < 1 else b * ColorVisualizer.MAX_INTENSITY

        self.rv = 0
        self.bv = 0
        self.gv = 0     
        # 5 is a magic number. I know. Get over it.
        self.signal_history = deque(maxlen=5)   
        self.sig_time_history = deque([time.time()], maxlen=5)

        # 3 for RGB 
        self.signal_intensity_maxes = [ColorVisualizer.SIGNAL_INTENSITY_MAX_START] * 3

    

    def tuple(self):
        #print(str(self.red) + ', ' + str(self.green) + ', ' + str(self.blue))
        return (self.red, self.green, self.blue)

    def _bounds_check(self, r, g, b):
        r = min(r, ColorVisualizer.MAX_INTENSITY)
        g = min(g, ColorVisualizer.MAX_INTENSITY)
        b = min(b, ColorVisualizer.MAX_INTENSITY)

        r = max(r, ColorVisualizer.MIN_INTENSITY)
        g = max(g, ColorVisualizer.MIN_INTENSITY)
        b = max(b, ColorVisualizer.MIN_INTENSITY)

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

    def _choose_rgb_signals(self, freq_amps, dt):
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




    def update_colors(self, freq_amps):

        dt = time.time() - self.sig_time_history[-1]
        self.sig_time_history.append(time.time())

        rgb_raw = self._choose_rgb_signals(freq_amps, dt)

        self.signal_intensity_maxes = [max(c,m) for c, m in zip(rgb_raw, self.signal_intensity_maxes)]
        r, g, b = [x/m for x, m in zip(rgb_raw, self.signal_intensity_maxes)]
        smooth_r, smooth_g, smooth_b = self._smooth(r, g, b)
        #print(smooth_r, smooth_g, smooth_b)

        excited_r = max(smooth_r, r)

        #print(Color.ACCELERATION * smooth_g)
        r_fall_const = 1#max(self.signal_intensity_maxes[0]/ColorVisualizer.R_CONST, 1)
        g_fall_const = 1#max(self.signal_intensity_maxes[1]/ColorVisualizer.G_CONST, 1)
        b_fall_const = 1#max(self.signal_intensity_maxes[2]/ColorVisualizer.B_CONST, 1)

        print(r_fall_const, g_fall_const, b_fall_const)

        self.rv = ColorVisualizer.GRAVITY * r_fall_const + ColorVisualizer.ACCELERATION * excited_r 
        self.gv = ColorVisualizer.GRAVITY * g_fall_const + ColorVisualizer.ACCELERATION * smooth_g 
        self.bv = ColorVisualizer.GRAVITY * b_fall_const + ColorVisualizer.ACCELERATION * smooth_b 

        for i, m_i in enumerate(self.signal_intensity_maxes):
            if m_i > ColorVisualizer.SIGNAL_INTENSITY_DRAG:
                drag = ColorVisualizer.SIGNAL_INTENSITY_DRAG 
                if m_i > ColorVisualizer.SIGNAL_INTENSITY_THRESHOLD:
                    drag *= ColorVisualizer.RGB_CONST[i]
                self.signal_intensity_maxes[i] = max(ColorVisualizer.SIGNAL_INTENSITY_MAX_START, m_i - drag)


        self.red += self.rv 
        self.green += self.gv
        self.blue += self.bv

        self.red, self.green, self.blue = self._bounds_check(self.red, self.green, self.blue)
