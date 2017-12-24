import pygame
import colorsys
import time


BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

SURFACE_SIZE = (400, 400)

MAX_VALUE = 255

pygame.init()

def init():
    width, height = (400, 400)
    black_color = 0,0,0
    screen = pygame.display.set_mode(SURFACE_SIZE)
    pygame.display.set_caption('circle vis')
    screen.fill(black_color)
    pygame.display.flip()

def create_rings(screen, color_list, min_circle_size=10):
    center = tuple(x/2 for x in SURFACE_SIZE)
    max_circle_size = int(max(center) * (2**(1.0/2)))
    for i, color in enumerate(color_list):
        radius = min_circle_size + ((max_circle_size - min_circle_size) * (len(color_list) - i) / len(color_list)) 

        pygame.draw.circle(screen, color, center, radius, 0)
    pygame.display.flip()

if __name__ == '__main__':
    
    running = True
    starting_val = 0.0
    while running:
        num_colors = 100
        colors = []
        for i in range(num_colors):
            colors.append( tuple(int(x * MAX_VALUE) for x in colorsys.hsv_to_rgb(float(i)/num_colors + starting_val, 1, 1)))
        create_rings(screen, colors)
        time.sleep(0.1)
        starting_val -= 0.01
        starting_val %= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
