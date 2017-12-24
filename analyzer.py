import pygame

BAR_WIDTH = 40
NOTES = 87

class Analyzer:
    def __init__(self):
        pygame.init()
        self.width, self.height = (300, 200)
        black_color = 0,0,0
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(black_color)
        pygame.display.flip()

    def update(self, visualizer):
        self.screen.fill( visualizer.tuple() )
        pygame.display.flip() 

