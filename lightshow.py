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
import stream
from subprocess import call
from time import sleep 

is_pi = False
try:
    import pigpio
    is_pi = True
    print "is pi"
except:
    print "is not pi. is mac"

# global variables
pi = None
analyzer = None
light_visualizer = HSVVisualizer(10, 10, 10)

# for raspberry pi
if is_pi:
    pi = pigpio.pi()
# for development on mac
else:
    analyzer = analyzer_mod.CircleAnalyzer(light_visualizer)

# The GPIO Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

def update_colors(red, green, blue):
    global is_pi
    if is_pi:
        pi.set_PWM_dutycycle(RED_PIN, int(red))
        pi.set_PWM_dutycycle(GREEN_PIN, int(green))
        pi.set_PWM_dutycycle(BLUE_PIN, int(blue))         

def visualize(light_visualizer):
    global is_pi
    try:
        while True: 
            update_colors(*light_visualizer.tuple())
    except KeyboardInterrupt:
        if is_pi:
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
        audio_stream = stream.FileStream(sys.argv[1])
    else:
        audio_stream = stream.Stream()
        lights_thread = threading.Thread(target=visualize, args=(light_visualizer,))
        lights_thread.daemon = True
        lights_thread.start()

    light_visualizer.attach_stream(audio_stream)
    
    vis_thread = threading.Thread(target=light_visualizer.visualize)
    vis_thread.daemon = True
    vis_thread.start()

    if not is_pi: 
        analyzer.update()

    vis_thread.join()
    print("done")
