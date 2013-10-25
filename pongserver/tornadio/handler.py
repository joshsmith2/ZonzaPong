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
    players = set()

    def __init__(self, *args, **kwargs):
        super(IOConnection, self).__init__(*args, **kwargs)
        self.l = logging.info

    @event
    def register(self):
        paddle_id = None
        if len(self.players) == 0:
            paddle_id = 1
        elif len(self.players) == 1:
            paddle_id = 2
        if paddle_id:
            self.emit("register", paddle_id)

    @event
    def paddle_move(self, paddle, paddle_id):
        self.emit()

    @event
    def ping(self):
        self.l("Ping EVENT received ! --> Answering back with a 'pingback' event")
        self.emit("pingback")

    @event
    def move(self, position):
        self.l("Move EVENT received ! --> received position is: {}".format(position))
        self.emit("pingback", position)

    @event
    def game(self, ball, paddle1, paddle2):
        self.l("---- GAME Event ----")
        self.l(ball)
        self.l(paddle1)
        self.l(paddle2)
        self.emit("game", {
            "ball": ball,
            "paddle1": paddle1,
            "paddle2": paddle2,
        })

    def on_open(self, info):
        self.players.add(self)
        l("Connected !")
        self.emit('toto', {"msg":"Connected"})

    def on_message(self, message):
        # Pong message back
        for p in self.players:
            p.send(message)

    def on_close(self):
        self.players.remove(self)

    def _check_token(self, token):
        return True if self.api_key == token else False
