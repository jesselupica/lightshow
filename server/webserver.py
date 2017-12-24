import json
import os.path
import select
import socket
import sys
from deviceModel import Device

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind(('localhost', 5001))
server.listen(5)
inputs = [server]
outputs = []

conn_to_device = {}
registered_devices = []
device_index = {}

registration_file = "registered_devices.json"
    
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
    data = s.recv(1024)
    print data
    if data:
        try:
            client_message = json.loads(data)
        except ValueError:
            return 
        if "registration" in client_message:
            register_device(s, client_message)
                
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

if __name__ == "__main__":
    run_server()
