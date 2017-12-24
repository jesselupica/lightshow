import json
import socket
import uuid

SERVER_IP = "104.131.78.170"
SERVER_PORT = "5001"

class Client(object):
    def __init__(self, server_ip, server_port, visualizer):
        super(Client, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.registration = None
        self.vis = visualizer
        self.commands = {'hue' : self.set_hue, 
                        'static color' : self.set_static_color,
                        'toggle visualizer' : self.toggle_visualizer, 
                        'on/off' : self.toggle_lights,
                        'fade' : self.toggle_fade,
                        'sat' : self.set_sat,
                        'brightness' : self.set_brightness}
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
        sock.connect((self.server_ip, self.server_port))
        sock.send(json.dumps(self.registration))

        while True: 
            req_str = sock.recv(1024)
            if not req_str:
                break
            req = json.loads(req_str)
            print req
            self.handle_req(req)

    def handle_req(self, req):
        command = req["command"]["function"]
        args = req["command"]["args"]
        commands[command](*args)

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


if __name__ == '__main__':
    from HSVVisualizer import HSVVisualizer
    vis = HSVVisualizer(0,0,0)
    cli = Client('localhost', 5001, vis)
    cli.run_client()

