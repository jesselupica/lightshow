import json
import os.path
import select
import socket
import sys
from deviceModel import Device
from flask import Flask, request, render_template, send_from_directory
from threading import Thread
from flask_cors import CORS

app = Flask(__name__, static_folder='lightshow-frontend/build/static/', template_folder='lightshow-frontend/build/')
CORS(app)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind(('', 5001))
server.listen(5)
inputs = [server]
outputs = []

conn_to_device = {}
registered_devices = []
device_index = {}

registration_file = "registered_devices.json"

## TODO: Define a get state method

def remove_device_from_registration_list(device_id, r=registered_devices):
    a = r
    registered_devices = [r for r in a if r.registration_id != device_id] 

def load_registered_devices():
    if os.path.isfile(registration_file):
        with open(registration_file, mode="r+") as f:
            registration_data = json.loads(f.read())
            for device_json in registration_data:
                d = Device(device_json["id"], device_json["nickname"])
                registered_devices.append(d)
                device_index[device_json["id"]] = d

def save_registered_devices():
    with open(registration_file, mode="w+") as f:
        f.write(json.dumps([d.to_json() for d in registered_devices]))

def run_server():
    load_registered_devices()
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server:
                print "hello friend"
                add_input_connection(s)
            else:
                if s not in outputs:
                    outputs.append(s)
                handle_request(s)
        for s in writable:
            if s in conn_to_device:
                device = conn_to_device[s]
                device.send_enqueued_messages(s)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            # remove s from devices if device
            if s in conn_to_device:
                del conn_to_device[s]

def add_input_connection(s):
    connection, client_address = s.accept()
    connection.setblocking(0)
    inputs.append(connection)

def handle_request(s):
    try:
        data = s.recv(1024)
    except:
        return
    print data + " | "
    if data:
        for message in data.split('\n'):
            try:
                client_message = json.loads(message)
            except ValueError as e:
                print "value error", e, message 
                continue 
            if "registration" in client_message:
                register_device(s, client_message)
            if "state" in client_message:
                print "we're here", client_message
                device_id = client_message['id']
                device_index[device_id].state = client_message['state']
                    
            # may have to change with auth
            if "device" in client_message and client_message['device'] in device_index:
                device_id = client_message['device']
                device_index[device_id].messages.append(client_message['command'])
    else:
        # if s is a device, remove it from the list
        if s in outputs:
            outputs.remove(s)
        inputs.remove(s)
        s.close()
        if s in conn_to_device:
            del conn_to_device[s]

def register_device(socket_conn, client_message):
    new_device_registration = client_message['registration']

    if new_device_registration not in device_index:
        dev = Device(new_device_registration)
        registered_devices.append(dev)
        device_index[new_device_registration] = dev
    else:
        dev = device_index[new_device_registration]
    conn_to_device[socket_conn] = dev
    save_registered_devices()

@app.route('/device/<device_id>', methods=['POST', 'GET'])
def show_user_profile(device_id):
    # may have to change with auth
    if request.method == 'POST':
        data = json.loads(request.data)
        if device_id in device_index:
            device_index[device_id].messages.append(data["command"])
        return "Message relayed"
    elif request.method == 'GET':
        return json.dumps(device_index[device_id].to_json())

@app.route('/device/remove/<device_id>', methods=['POST'])
def remove_device(device_id):
    if request.method == 'POST':
        try:
            registered_devices.remove(device_index[device_id])
            del(device_index[device_id])
        except:
            print registered_devices
        remove_device_from_registration_list(device_id)
        save_registered_devices()
    return 'success', 200
    
@app.route('/device/rename/<device_id>', methods=['POST'])
def rename_device(device_id):
    if request.method == 'POST':
        data = json.loads(request.data)
        device_index[device_id].nickname = data['nickname']
        save_registered_devices()
    return 200
        
@app.route("/devices")
def get_devices():
    return json.dumps([d.to_json() for d in registered_devices])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>') # serve whatever the client requested in the static folder
def serve_static(path):
    return send_from_directory('lightshow-frontend/build/static', path)

@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('lightshow-frontend/build/', 'service-worker.js')
        
@app.route('/favicon.ico')
def serve_fav():
    return send_from_directory('lightshow-frontend/build/', 'favicon.ico')

@app.errorhandler(500)
def internal_server_error(e):
    print e

if __name__ == "__main__":
    t = Thread(target=app.run, kwargs={"host":"0.0.0.0", "port" : 80})
    t.daemon = True
    t.start()
    run_server()
    
