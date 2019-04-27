# HTTPServer Things
from webserver.HTTPRequestHandler import HTTPRequestHandler
from threading import Thread
from http.server import HTTPServer
from functools import partial
import config

class ThreadedHTTPServer(Thread):
    def __init__(self,rgbC):
        Thread.__init__(self)
        self.rgbC = rgbC
        self.daemon = True
        self.start()
    
    def run(self):
        httpd = HTTPServer(("", config.SocketBindPort),partial(HTTPRequestHandler, self.rgbC))
        httpd.serve_forever()