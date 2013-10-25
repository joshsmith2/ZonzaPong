'''
Created on 6 juin 2012

@author: Sora
'''

from tornadio2.conn import event
import logging
import tornadio2


l = logging.info

class IOConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    participants = set()

    def __init__(self, *args, **kwargs):
        super(IOConnection, self).__init__(*args, **kwargs)
        self.l = logging.info


    @event
    def ping(self):
        self.l("Ping EVENT received ! --> Answering back with a 'pingback' event")
        self.emit("pingback")

    @event
    def move(self, position):
        self.l("Move EVENT received ! --> received position is: {}".format(position))
        self.emit("pingback", position)

    def on_open(self, info):
        self.participants.add(self)
        l("Connected !")
        self.emit('toto', {"msg":"Connected"})

    def on_message(self, message):
        # Pong message back
        for p in self.participants:
            p.send(message)

    def on_close(self):
        self.participants.remove(self)

    def _check_token(self, token):
        return True if self.api_key == token else False
