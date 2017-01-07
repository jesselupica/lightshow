from __future__ import division
import sys
import os
#from RGBVisualizer import RGBVisualizer
from HSVVisualizer import HSVVisualizer
from recording import Recording
from subprocess import call

# this runs on a pi, so make sure you update the name of your pi to the correct name
pi_name = 'raspberrypi'

light_mod_name = None
uname = os.uname()
if uname[1] == pi_name and uname[0] == 'Linux':
    light_mod_name = 'pigpio'
else: 
    light_mod_name = 'pygame'

light_source = __import__(light_mod_name)

# The Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

# global variables
pi = None
screen = None

uname = os.uname()
if uname[1] == pi_name and uname[0] == 'Linux':
    pi = light_source.pi()
    print(pi)
else: 
    width, height = (300, 200)
    black_color = 0,0,0
    screen = light_source.display.set_mode((width, height))
    screen.fill(black_color)
    light_source.display.flip()

def update_colors(red, green, blue):
    uname = os.uname()
    if uname[1] == pi_name and uname[0] == 'Linux':
        pi.set_PWM_dutycycle(RED_PIN, int(red))
        pi.set_PWM_dutycycle(GREEN_PIN, int(green))
        pi.set_PWM_dutycycle(BLUE_PIN, int(blue))
    else: 
        screen.fill( (red, green, blue) )
        light_source.display.flip()    

def visualize(file_name=None):
    try:
        # Start out white
        music = Recording(file_name=file_name, playback=True if file_name else False)
        chunk_size, rate = music.spec()

        light_visualizer = HSVVisualizer(255, 255, 255)

        while music.still_playing(): 
            sound_data = music.get_chunk()
            if not sound_data:
                break

            light_visualizer.visualize(sound_data, rate)
            update_colors(*light_visualizer.tuple())
    except KeyboardInterrupt:
        pi.set_PWM_dutycycle(RED_PIN, 0)
        pi.set_PWM_dutycycle(GREEN_PIN, 0)
        pi.set_PWM_dutycycle(BLUE_PIN, 0)
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    print("Start recording...")
    if len(sys.argv) >= 2:
        visualize(file_name=sys.argv[1])
    else:
        visualize()
    print("done")
