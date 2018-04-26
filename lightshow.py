from __future__ import division
import sys
import termios
import tty
import os
import traceback
import threading
import deviceClient
import pygame
import analyzer as analyzer_mod 
from HSVVisualizer import HSVVisualizer
from globalvars import light_visualizer
import stream
from globalvars import light_visualizer
from subprocess import call
from time import sleep 


# this runs on a pi, so make sure you update the name of your pi to the correct name
pi_name = 'raspberrypi'

try:
    import pigpio
except:
    pass
# global variables
pi = None
screen = None

uname = os.uname()
analyzer = None
if uname[1] == pi_name and uname[0] == 'Linux':
    pi = pigpio.pi()
    print(pi)
else:
    analyzer = analyzer_mod.CircleAnalyzer(light_visualizer)

# The Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

def update_colors(red, green, blue):
    #print (red, blue, green)
    uname = os.uname()
    if uname[1] == pi_name and uname[0] == 'Linux':
        pi.set_PWM_dutycycle(RED_PIN, int(red))
        pi.set_PWM_dutycycle(GREEN_PIN, int(green))
        pi.set_PWM_dutycycle(BLUE_PIN, int(blue))         

def visualize(light_visualizer, file_name=None):
    try:
	print "starting here"
        if file_name != None:
            music = stream.FileStream(file_name)
        else:
            music = stream.Stream()
        print "then"
	chunk_size, rate = music.spec()
        while True: 
            sound_data = music.get_chunk()
            if not sound_data:
                continue
                
            if light_visualizer.is_asleep:
                sleep(0.1)
            if light_visualizer.is_off:
                sleep(0.1)

            light_visualizer.visualize(sound_data, rate)
            #analyzer.update(light_visualizer)
            update_colors(*light_visualizer.tuple())

    except KeyboardInterrupt:
        if uname[1] == pi_name and uname[0] == 'Linux':
            pi.set_PWM_dutycycle(RED_PIN, 0)
            pi.set_PWM_dutycycle(GREEN_PIN, 0)
            pi.set_PWM_dutycycle(BLUE_PIN, 0)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        pass

if __name__ == '__main__':
    print("Start recording...")

    cli = deviceClient.Client(light_visualizer)

    cli_thread = threading.Thread(target=cli.run_client)
    cli_thread.daemon = True
    cli_thread.start()
    
    if len(sys.argv) >= 2:
        vis_thread = threading.Thread(target=visualize, args=(light_visualizer,) ,kwargs={'file_name' : sys.argv[1]})
    else:
        vis_thread = threading.Thread(target=visualize, args=(light_visualizer,))
    
    vis_thread.daemon = True
    vis_thread.start()

    if not (uname[1] == pi_name and uname[0] == 'Linux'): 
        analyzer.update()

    vis_thread.join()
    print("done")
