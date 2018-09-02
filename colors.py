from itertools import cycle

color_table = {'RED': 1, 'ORANGE':0.038888, 'GREEN': 0.3333, 'TEAL':0.5527777,
 'BLUE': 0.66666, 'PURPLE': 0.783333, 'PINK':0.9444  }


class NaiveHueSelector:
    def __init__(self):
        self.hues = cycle(sorted(color_table.values()))
        self.curr = None 
    def next(self, mag):
        print "next"
        if mag > 3.5: 
            self.curr = next(self.hues)
        return self.curr

class ColorPalleteHueSelector:
    def __init__(self):
        pass

    def next(self, mag):
        pass