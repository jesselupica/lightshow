#!/usr/bin/python3

import requests
import json

base_url = 'http://www.jesselupica.com'

def lambda_handler(event, context):
    devices = requests.get(base_url + '/devices').json()
    token = requests.post(base_url + '/auth/guest/init').text
    for d in devices:
        print(d['id'])
        data = { 
            'command': {"function": "on/off", "args": []}, 
            'auth_token': token
        }
        print(requests.post(base_url + '/device/' + d['id'], data=json.dumps(data)))
    return 'Hello from Lambda'

if __name__ == '__main__':
    lambda_handler(None, None)