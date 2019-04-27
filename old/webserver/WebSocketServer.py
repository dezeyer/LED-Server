from webserver.SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from webserver.HTTPWebSocketsHandler import HTTPWebSocketsHandler
from threading import Thread
from functools import partial

class ThreadedWebSocketServer(Thread):
    def __init__(self,effectController,rgbStripController):
        Thread.__init__(self)
        self.effectController = effectController
        self.rgbStripController = rgbStripController
        self.daemon = True
        self.stopped = False
        self.start()
    
    def run(self):
        server = SimpleWebSocketServer('', 8001, partial(HTTPWebSocketsHandler,self.effectController, self.rgbStripController))
        while not self.stopped:
            server.serveonce()
        print("ThreadedWebSocketServer stopped")

    def stop(self):
        self.stopped = True