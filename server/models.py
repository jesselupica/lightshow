import json

class FrontendClient:
    def __init__(self, auth_token, username, password, priv = 0, is_guest=False):
        self.is_admin = False
        self.username = username
        self.hashed_pass = hash(password)
        # three levels: 0 - can only observe, 1 - can control lights, 2 - admin
        self.priviledge_level = priv
        self.is_guest = is_guest

    def check_pass(self, password):
        return self.hashed_pass == hash(password)

    def to_json(self):
        return {"username" : self.username, 
                "is_admin" : self.is_admin, 
                "hashed_pass" : self.hashed_pass, 
                "priviledge_level" : self.priviledge_level }
        

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
            print "sending", message, "to", self.registration_id
            s.send(json.dumps(message) + '\n')
        self.messages = []

    def to_json(self):
        return {"id" : self.registration_id, "nickname" : self.nickname, "state" : self.state }