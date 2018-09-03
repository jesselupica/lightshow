import json
import hashlib
from collections import namedtuple
from flask_sqlalchemy import SQLAlchemy


ClientDevice = namedtuple('ClientDevice', ['os', 'device', 'time_since_last_req'])

class FrontendClient:
    def __init__(self, auth_token, username, password, 
            priv = 0, is_admin=False, is_guest=False, pass_already_hashed=False, ):
        self.is_admin = is_admin
        self.username = username
        if not pass_already_hashed:
            pass_m = hashlib.sha256()
            pass_m.update(password)
            self.hashed_pass = pass_m.hexdigest()
        else:
            self.hashed_pass = password
        
        # three levels: 0 - can only observe, 1 - can control lights, 2 - admin
        self.privilege_level = priv
        self.is_guest = is_guest
        self.auth_token = auth_token

    def check_pass(self, password):
        return self.hashed_pass == hashlib.sha256(password).hexdigest()

    def to_json(self):
        return {"username" : self.username, 
                "is_admin" : self.is_admin, 
                "hashed_pass" : self.hashed_pass, 
                "privilege_level" : self.privilege_level,
                "auth_token" :  self.auth_token}
        

class Device(object):
    """docstring for Device"""
    def __init__(self, r_id, nickname=""):
        super(Device, self).__init__()
        self.registration_id = r_id
        self.nickname = nickname
        self.state = {}
        self.messages = []

    def send_enqueued_messages(self, s):
        for message in self.messages:
            s.send(json.dumps(message) + '\n')
        self.messages = []

    def to_json(self):
        return {"id" : self.registration_id, "nickname" : self.nickname, "state" : self.state }
