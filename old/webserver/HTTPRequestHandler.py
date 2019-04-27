from http.server import BaseHTTPRequestHandler, HTTPServer
import rgbUtils.RGBStipContollerJsonConverter as rgbCJson
from pathlib import Path
from mimetypes import guess_type
from os import curdir, sep
import json

from rgbUtils.debug import debug

class HTTPRequestHandler(BaseHTTPRequestHandler):
    rgbC = None

    def __init__(self, rgbC, *args, **kwargs):
        self.rgbC = rgbC
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        try:
            if "/api/" in self.path:
                # set response header application/json when calling the api
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                if "/getEffects" in self.path:
                    self.wfile.write(json.dumps({'result': rgbCJson.getEffects(self.rgbC)}).encode(encoding='utf_8'))

                if "/getRGBStrips" in self.path:
                    self.wfile.write(json.dumps({'result': rgbCJson.getRGBStrips(self.rgbC)}).encode(encoding='utf_8'))

                if "/getEffectThreads" in self.path:
                    self.wfile.write(json.dumps({'result': rgbCJson.getEffectThreads(self.rgbC)}).encode(encoding='utf_8'))

            else:
                #Get files as requested from htdocs, set mimetype
                request = curdir + sep + "htdocs" + self.path
                debug(request)

                if Path(request).is_dir():
                    debug("isdir: "+request)
                    if not request[-1:] == "/":
                        debug("no /: "+request)
                        request += "/"
                    request += "index.html"
                debug("fi request: "+request)

                mimetype = guess_type(request)[0]
                f = open(request, 'rb')
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    def do_POST(self):
        try:
            if "/api/" in self.path:
                self.send_response(200)
                data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
                self.end_headers()
                print(data)
                if "/startEffect" in self.path:
                    enabledRGBStrips = []
                    for rgbStripObject in data['rgbStrips']:
                        if rgbStripObject[1]:
                            enabledRGBStrips.append(self.rgbC.getRGBStrips()[int(rgbStripObject[0])])
                    
                    self.rgbC.startEffect(self.rgbC.getEffects()[data['effect']],enabledRGBStrips,data['params'])
                if "/moveRGBStripToEffectThread" in self.path:
                    print(data)
                    self.rgbC.moveRGBStripToEffectThread(self.rgbC.getRGBStrips()[data['rgbStrip']],self.rgbC.getEffectThreads()[data['effectThread']])
                if "/updateEffectParams" in self.path:
                    result = {}
                    print(data)
                self.wfile.write("OK".encode(encoding='utf_8'))
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def log_message(self, format, *args):
        return