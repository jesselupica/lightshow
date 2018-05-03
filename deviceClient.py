import json
import socket
import uuid
import time
import os
import sys

#SERVER_IP = "104.131.78.170"
SERVER_DOMAIN = 'jesselupica.com'
SERVER_PORT = 5001

CLIENT_LOCATION = '/home/pi/Public/lightshow/'

class Client(object):
    def __init__(self, visualizer, server_ip=SERVER_DOMAIN, server_port=SERVER_PORT):
        super(Client, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.registration = None
        self.vis = visualizer
        # value is a tuple of the function and privilege level needed to 
        # run the function
        self.commands = {'hue' : (self.set_hue, 1), 
                        'static color' : (self.set_static_color, 1),
                        'toggle visualizer' : (self.toggle_visualizer, 1), 
                        'on/off' : (self.toggle_lights, 1),
                        'fade' : (self.toggle_fade, 1),
                        'sat' : (self.set_sat,1),
                        'brightness' : (self.set_brightness, 1),
                        'mode' : (self.set_mode, 1),
                        'fade_speed' : (self.set_fade_speed, 1),
                        'git pull' : (self.pull_from_repo, 2)}
        self.register_device()

    def register_device(self):
        try:
            with open("device_id.json", mode="r") as f: 
                data = f.read()
                self.registration = json.loads(data)
        except IOError:
            print "writing new id"
            with open("device_id.json", mode="w") as f:
                self.registration = {"registration" : str(uuid.uuid1()) }
                f.write(json.dumps(self.registration))

    def run_client(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
            try: 
                sock.connect((self.server_ip, self.server_port))
            except socket.error as e:
                # don't overwhelm the server when it goes down
                sleep(0.1)
                print e
            else:
                try:
                    sock.send(json.dumps(self.registration) + "\n")
                except socket.error as e:
                    continue
                self.send_state(sock)

                while True: 
                    try: 
                        req_str = sock.recv(1024)
                    except socket.error: 
                        break
                    if not req_str:
                        break
                    for r in req_str.split('\n'):
                        try: 
                            req = json.loads(r)
                        except ValueError as e:
                            continue 
                        self.handle_req(req)
                        self.send_state(sock)

    def handle_req(self, req):
        command = req["function"]
        args = req["args"]
        privilege_lvl = req["client_privilege_level"]
        if self.commands[command][1] <= privilege_lvl:
            try:
                self.commands[command][0](*args)
            except Exception as e:
                print("error", e)

    def send_state(self, sock):
        mess = {"id" : self.registration["registration"], "state" : self.vis.get_state()}
        try:
            sock.send(json.dumps(mess) + '\n')
        except socket.error:
            return

    def set_sat(self, sat):
        self.vis.set_sat(float(sat))

    def set_hue(self, hue):
        self.vis.set_hue(float(hue))

    def toggle_visualizer(self):
        if self.vis.mode == 'VISUALIZE_MUSIC':
            self.vis.set_color(self.vis.static_color)
        else:
            self.vis.turn_on_music_visualization()

    def toggle_lights(self):
        if self.vis.mode != 'OFF':
            self.vis.turn_off_lights()
        else: 
            self.vis.turn_on_music_visualization()

    def toggle_fade(self):
        if self.vis.mode == 'FADE':
            self.vis.turn_on_music_visualization()
        else:
            self.vis.turn_on_fade()

    def set_static_color(self, color):
        self.vis.set_color(color.upper()) 

    def set_brightness(self, val):
        self.vis.set_brightness(float(val))

    def set_mode(self, mode, args):
        if mode == 'off':
            self.vis.turn_off_lights()
        elif mode == 'vis':
            self.vis.turn_on_music_visualization()
            self.vis.set_brightness(args["brightness"])
            self.vis.set_sat(args["sat"])
        elif mode == 'fade':
            self.vis.turn_on_fade()
            self.vis.set_fade_speed(args["fade_speed"])
        else:
            self.vis.set_color(args["color"].upper())

    def set_fade_speed(self, speed):
        self.vis.set_fade_speed(float(speed))

    def pull_from_repo(self):
        try:
            os.chdir(CLIENT_LOCATION)
            os.system('git stash && git checkout master && git pull')
            for i in range(5):
                self.vis.turn_off_lights()
                time.sleep(0.5)
                self.vis.turn_on_fade()
                time.sleep(0.5)
            print("hey we didn't crash")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    from HSVVisualizer import HSVVisualizer
    vis = HSVVisualizer(0,0,0)
    if len(sys.argv) > 2:
        print sys.argv[1], sys.argv[2]
        cli = Client(vis, sys.argv[1], int(sys.argv[2]))
    else: 
        cli = Client(vis)
    cli.run_client()

