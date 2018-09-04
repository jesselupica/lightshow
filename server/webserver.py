import json
import os.path
import select
import socket
import sys
import uuid
import time
from collections import OrderedDict
from models import Device, FrontendClient
from flask import Flask, request, render_template, send_from_directory
from threading import Thread
from flask_cors import CORS
import hashlib
from gevent.pywsgi import WSGIServer

app = Flask(__name__)#, static_folder='lightshow-frontend/build/static/', template_folder='lightshow-frontend/build/')
#CORS(app)

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
client_file = "clients.json"

clients = OrderedDict()
ADMIN_PRIV_LVL = 2

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

def load_client_credentials():
    if os.path.isfile(client_file):
        with open(client_file, mode="r+") as f:
            client_data = json.loads(f.read())
            for client_json in client_data:
                cli = FrontendClient(client_json["auth_token"], client_json["username"], client_json["hashed_pass"], 
                    priv=client_json["privilege_level"], 
                    is_admin=client_json["is_admin"], 
                    pass_already_hashed=True)
                clients[client_json["auth_token"]] = cli

def save_registered_devices():
    with open(registration_file, mode="w+") as f:
        f.write(json.dumps([d.to_json() for d in registered_devices]))

def save_client_credentials():
    with open(client_file, mode="w+") as f:
        f.write(json.dumps([c.to_json() for auth, c in clients.items() if not c.is_guest]))

def clear_guests():
    clients = OrderedDict([tuple(k, v) for k,v in clients.items() if not v.is_guest])

def create_guest_user():
    guest_token = str(uuid.uuid1())
    # create this so that people can't log in as guests i give permissions to
    usr_m = hashlib.sha256()
    pass_m = hashlib.sha256()
    
    usr_m.update(str(time.time()))
    pass_m.update(str(time.time() + 1))
    clients[guest_token] = FrontendClient(guest_token, usr_m.digest(), pass_m.digest(), is_guest=True)
    return guest_token

def create_user(username, password):
    auth_token = str(uuid.uuid1())
    clients[auth_token] = FrontendClient(auth_token, username, password)
    return auth_token

def user_already_exists(username):
    for cli in clients.values():
        if cli.username == username:
            return True
    return False

def run_server():
    print("starting server")
    load_registered_devices()
    load_client_credentials()
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server:
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
    print("new connection from client", connection.getpeername())
    inputs.append(connection)

def handle_request(s):
    try:
        data = s.recv(1024)
    except:
        return
    if data:
        for message in data.split('\n'):
            try:
                client_message = json.loads(message)
            except ValueError as e:
                print("value error", e, message)
                continue 
            if "registration" in client_message:
                register_device(s, client_message)
            if "state" in client_message:
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

@app.route('/', methods=['GET'])
@app.route('/lights')
@app.route('/login')
@app.route('/signup')
def path_index():
    #return render_template('index.html')
    return "Hello there!"
    
@app.route('/<path:path>')
def serve_path(path):
    return send_from_directory('/var/www/jesselupica', path)

@app.route('/static/<path:path>') # serve whatever the client requested in the static folder
def serve_static(path):
    return send_from_directory('lightshow-frontend/build/static', path)

@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('lightshow-frontend/build/', 'service-worker.js')
        
@app.route('/favicon.ico')
def serve_fav():
    return send_from_directory('lightshow-frontend/build/', 'favicon.ico')

@app.route('/device/<device_id>', methods=['POST', 'GET'])
def show_user_profile(device_id):
    # may have to change with auth
    if request.method == 'POST':
        data = json.loads(request.data)
        data["command"]["client_privilege_level"] = 2 #clients[data["auth_token"]].privilege_level
        if device_id in device_index:
            device_index[device_id].messages.append(data["command"])
        return "Message relayed"
    elif request.method == 'GET':
        return json.dumps(device_index[device_id].to_json())

@app.route('/device/remove/<device_id>', methods=['POST'])
def remove_device(device_id):
    if request.method == 'POST':
        data = json.loads(request.data)
        if clients[data["auth_token"]].is_admin:
            try:
                registered_devices.remove(device_index[device_id])
                del(device_index[device_id])
            except:
                print(registered_devices)
            remove_device_from_registration_list(device_id)
            save_registered_devices()
            return "", 200
        else:
            return "", 403
    
@app.route('/device/rename/<device_id>', methods=['POST'])
def rename_device(device_id):
    if request.method == 'POST':
        data = json.loads(request.data)
        if clients[data["auth_token"]].is_admin:
            device_index[device_id].nickname = data['nickname']
            save_registered_devices()
            return "", 200
        else: 
            return "", 403
        
@app.route("/devices")
def get_devices():
    return json.dumps([d.to_json() for d in registered_devices])

@app.route('/auth/init', methods=['POST'])
def auth_init():
    if request.method == 'POST':
        data = json.loads(request.data)
        if not user_already_exists(data['username']) and  not data['username'] == '' and not data['password'] == '':
            auth_token = create_user(data['username'], data['password'])
            save_client_credentials()
            return auth_token, 200
        else:
            return "", 400
    return "", 400

@app.route('/auth/guest/init', methods=['POST'])
def auth_guest_init():
    return create_guest_user()

@app.route('/auth/user/devicedata', methods=['POST'])
def auth_get_device_data():
    if request.method == 'POST':
        data = json.loads(request.data)
        if user_already_exists(data['username']) and clients[data['auth_token']].username == data['username']:
            clients[data['auth_token']].device_features = data['device']
        return '', 200

@app.route('/auth/verify', methods=['POST'])
def auth_verify():
    if request.method == 'POST':
        found = False
        auth = ''
        data = json.loads(request.data)
        for auth_token, cli in clients.items():
            if data["username"] == cli.username:
                print(data["password"], hashlib.sha256(data['password']).hexdigest())
                print(cli.hashed_pass)
                if cli.check_pass(data["password"]):
                    auth = auth_token
                    found = True
                    break
        if found:
            return auth, 200
        else:
            return '', 403
    return '', 403

@app.route('/admin/users', methods=['GET'])
def get_users():
    data = json.loads(request.headers['params'])
    if clients[data["auth_token"]].is_admin:
        for cli in clients.values():
            {'username' : cli.username, 
            'device_info' : cli.device_features,
            'privilege_level' : cli.privilege_level}
        clis = [c.username for c in clients.items()]
        return json.dumps(clis), 200
    else:
        return '', 403

@app.route('/is_admin', methods=['POST'])
def is_admin():
    data = json.loads(request.data)
    if clients[data["auth_token"]].is_admin:
        return '', 200
    else:
        return '', 403
    
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    
if __name__ == "__main__":
    print "hello friends"
    t = Thread(target=run_server)
    t.daemon = True
    #    t.start()
    app.run(host='0.0.0.0')
    #http_server = WSGIServer(("0.0.0.0", 5000), app, certfile='/etc/letsencrypt/live/jesselupica.com/fullchain.pem', keyfile='/etc/letsencrypt/live/jesselupica.com/privkey.pem')
    #http_server.serve_forever()
    

    
