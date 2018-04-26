import pygame
import time
import colorsys

BAR_WIDTH = 40
NOTES = 87

SIDE_LENGTH = 400

black = [0, 0, 0]
white = [255, 0, 255]
red = [255, 0, 0]

class FadeAnalyzer:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        pygame.init()
        self.screen = pygame.display.set_mode([SIDE_LENGTH,SIDE_LENGTH])
        
        self.screen.fill(white)
        pygame.display.set_caption("My program")
        pygame.display.flip()
        
    def update(self):
        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill( self.visualizer.tuple() )
            pygame.display.flip()
            # yield
            time.sleep(0)
        
class CircleAnalyzer:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        pygame.init()
        self.screen = pygame.display.set_mode([SIDE_LENGTH,SIDE_LENGTH])
        self.max_radius = SIDE_LENGTH/2
        self.min_radius = 1
        self.screen.fill(black)
        pygame.display.set_caption("My program")
        pygame.display.flip()

    def update(self):
        center = (SIDE_LENGTH/2, SIDE_LENGTH/2)
        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
            if all( x == 0 for x in self.visualizer.tuple()):
                rgb_tup = (1, 1, 1)
            else:
                rgb_tup = self.visualizer.tuple()

            hsv = colorsys.rgb_to_hsv(*rgb_tup)
            color = [int(x * 255) for x in colorsys.hsv_to_rgb(hsv[0], hsv[1], 1)]
            radius = (hsv[2]/255 * (self.max_radius - self.min_radius) ) + self.min_radius 
            self.screen.fill(black)
            pygame.draw.circle(self.screen, color, center, int(radius), 0)
            pygame.display.flip()
            # yield
            time.sleep(0)
