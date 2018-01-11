import json

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