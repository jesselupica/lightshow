import json
import time
from itertools import cycle
from webcolors import hex_to_rgb
from colorsys import rgb_to_hsv
from spotify_integration import SpotifyIntegration

DEFAULT_HUE_CHASER_MULTIPLIER = 0.015
MAX_PALETTE_TIME = 45


class NaiveHueSelector:
    def __init__(self):
        self.hues = cycle(sorted(color_table.values()))
        self.curr = next(self.hues) 
        self.hue_multiplier = DEFAULT_HUE_CHASER_MULTIPLIER

    def next(self, mag):
        print "next", mag
        if mag > 3.5: 
            self.curr = next(self.hues)
        return self.curr

    def get_multiplier(self):
        return self.hue_multiplier

class ColorPalleteHueSelector:
    class Palette:
        def __init__(self, p):
            self.colors = p['colors']
            self.hue_multiplier = p['hue multiplier']
            self.name = p['name']
            self.is_chill = p['is chill']

    def __init__(self, spotify_integration=None):
        self.hue_multiplier = DEFAULT_HUE_CHASER_MULTIPLIER
        self.color_palettes = []
        
        self.timer = 0
        if spotify_integration is None:
            self.spotify_integ = SpotifyIntegration()
            self.spotify_integ.detection_failure = True
        else:
            self.spotify_integ = spotify_integration

        with open('color_palettes.json') as f:
            dat = json.load(f)
            macros = dat['macros']
            palettes = dat['palettes']
            for i, p in enumerate(palettes):
                pal = self.Palette(p)
                # replace all instances of macros with their colors
                pal.colors = [c if c not in macros else macros[c] for c in pal.colors]
                # convert to hsv color system, make colors cyclable  
                pal.colors = cycle([self.hex_to_hsv(c) for c in pal.colors])
                self.color_palettes.append(pal)

        self.color_palettes = cycle(self.color_palettes)
        # initialize easily 
        self.next(float('inf'))

    def hex_to_hsv(self, color):
        if not color[0] == '#':
            color = '#' + color
        return rgb_to_hsv(*[float(c) for c in hex_to_rgb(color)])

    def next(self, mag):
        print "next", mag, time.time() - self.timer
        if (mag > 3.5 and time.time() - self.timer > 1.0) or time.time() - self.timer > MAX_PALETTE_TIME: 
            self.curr_pal = next(self.color_palettes)
            spotify_integ_offline = self.spotify_integ.detection_failure
            mismatched_mood = self.curr_pal.is_chill != self.spotify_integ.is_chill
            while not spotify_integ_offline and mismatched_mood:
                self.curr_pal = next(self.color_palettes)
                mismatched_mood = self.curr_pal.is_chill != self.spotify_integ.is_chill

            print "is chill", self.curr_pal.is_chill
            self.hue_multiplier = self.curr_pal.hue_multiplier
            print "palette change", self.curr_pal.name, time.time() - self.timer
            self.timer = time.time()

        self.curr_color = next(self.curr_pal.colors)
        return self.curr_color

    def get_multiplier(self):
        return self.hue_multiplier
