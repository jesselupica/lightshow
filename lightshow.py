from __future__ import division
import sys
import termios
import tty
import os
import traceback
import threading, thread
import webserver
from time import sleep
#from RGBVisualizer import RGBVisualizer
from HSVVisualizer import HSVVisualizer
from globalvars import light_visualizer
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

screen = light_source.display.set_mode((500, 500))
screen.fill((0,0,0))

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

def visualize(light_visualizer, file_name=None):
    try:
        # Start out white
        music = Recording(file_name=file_name, playback=True if file_name else False)
        chunk_size, rate = music.spec()

        while True: 
            sound_data = music.get_chunk()
            if not sound_data:
                print("no sound data")
                continue

            if light_visualizer.is_asleep:
                sleep(1)
            if light_visualizer.is_off:
                sleep(10)

            light_visualizer.visualize(sound_data, rate)
            update_colors(*light_visualizer.tuple())
    except KeyboardInterrupt:
        if uname[1] == pi_name and uname[0] == 'Linux':
            pi.set_PWM_dutycycle(RED_PIN, 0)
            pi.set_PWM_dutycycle(GREEN_PIN, 0)
            pi.set_PWM_dutycycle(BLUE_PIN, 0)
    except Exception as e:
        print(e)
        print(traceback.format_exc())

def get_ch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def control_visualizer_settings(light_visualizer):
    while True:
        c = get_ch()

        color_dict = {1: 'RED', 2: 'BLUE', 3: 'GREEN', 4: 'PURPLE', 5: 'AQUA'}
        
        if c == ' ':
            light_visualizer.toggle_music_visualization()
        elif c == '+':
            light_visualizer.update_bass_treble_ratio(True)
        elif c == '-':
            light_visualizer.update_bass_treble_ratio(False)
        elif c.isdigit():
            light_visualizer.set_color(color_dict[int(c)])
        elif c.lower() == 'c':
            break
    if light_visualizer.visualize_music:
        light_visualizer.toggle_music_visualization()
    light_visualizer.set_color('BLACK')
    update_colors(*light_visualizer.tuple())
    os._exit(0)

        
if __name__ == '__main__':
    print("Start recording...")
    print("Press 'C' to turn lights off")
    print("Press SPACE to toggle music visualization")
    print("Press the following buttons to change the lights to that color")
    print("1: RED, 2: BLUE, 3: GREEN, 4: PURPLE, 5: AQUA")

    t1 = threading.Thread(target=control_visualizer_settings, args=(light_visualizer,))
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=webserver.run_server, args=(light_visualizer,))
    t2.daemon = True
    t2.start()

    if len(sys.argv) >= 2:
        visualize(light_visualizer, file_name=sys.argv[1])
    else:
        visualize(light_visualizer)
    print("done")
