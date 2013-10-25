'''
Created on 6 juin 2012

@author: Sora
'''
from tornadio2 import server
from tornado.options import parse_command_line
from pongserver.tornadio.handler import IOConnection
from pongserver import settings

import sys
import tornadio2
import tornado
from tornado import template

class IndexHandler(tornado.web.RequestHandler):
    """Index Page handler : TESTING ONLY"""
    def get(self):
        self.render(settings.DOCUMENT_ROOT + '/resources/index.html')

class GameHandler(tornado.web.RequestHandler):
    """Game Page handler"""
    def get(self):
        token = self.get_argument('token')
        loader = template.Loader(settings.RESOURCES_ROOT)
        self.finish(loader.load('pong.html').generate(token=token))

class SocketIOHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.RESOURCES_ROOT + '/socket.io.js')

class WebSocketFileHandler(tornado.web.RequestHandler):
    def get(self):
        # Obviously, you want this on CDN, but for sake of
        # example this approach will work.
        self.set_header('Content-Type', 'application/x-shockwave-flash')
        with open(settings.RESOURCES_ROOT + '/WebSocketMain.swf', 'rb') as f:
            self.write(f.read())
            self.finish()

class StartGameHandler(tornado.web.RequestHandler):
    """Index Page handler : TESTING ONLY"""
    def get(self):
        self.render(settings.DOCUMENT_ROOT + '/resources/start.html')

    def post(self):
        file1 = self.request.files['image_file'][0]
        # now you can do what you want with the data, we will just save the file to an uploads folder
        output_file = open(settings.RESOURCES_ROOT + "/images/" + file1['filename'], 'w')
        output_file.write(file1['body'])
        self.redirect('/game/?token='+file1['filename'])

def application(argv=None):
    print "start"
    parse_command_line()
    if argv == None:
        argv = sys.argv

    # Create the server
    SocketRouter = tornadio2.router.TornadioRouter(IOConnection, dict(websocket_check=True))
    #  configure the Tornado application
    # currently only allow one command-line argument, the port to run on.
    port = int(argv[1]) if (len(argv) > 1) else settings.SOCKET_IO_PORT

    application = tornado.web.Application(
    SocketRouter.apply_routes([ (r"/", IndexHandler),
                                (r"/game/", GameHandler),
                                (r"/start/", StartGameHandler),
                                (r"/socket.io.js", SocketIOHandler),
                                (r"/resources/(.*)", tornado.web.StaticFileHandler,
                                    {"path": settings.RESOURCES_ROOT}),
                                (r"/WebSocketMain.swf", WebSocketFileHandler)
                            ]),
            flash_policy_port=8043,
            flash_policy_file=settings.DOCUMENT_ROOT + '/flashpolicy.xml',
            socket_io_port=port,
            )
    print("LocationMapper Server running on %s:%d" % (settings.SOCKET_IO_REMOTE_ADDR, port))
    return server.SocketServer(application)
