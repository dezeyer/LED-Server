import threading
import socketserver
import socket
import traceback
from time import sleep, time
import json
import struct


class ThreadedUDPServer(threading.Thread):
    def __init__(self, effectController, rgbStripController):
        threading.Thread.__init__(self, name="ThreadedUDPServer")
        self.effectController = effectController
        self.rgbStripController = rgbStripController
        self.daemon = True
        self.stopped = False
        self.start()
        self.udpClientGuardian = self.UDPClientGuardian()
        self.udpClientGuardian.start()
        UDPClients


    def run(self):
        self.server = socketserver.UDPServer(('', 8002), UDPStripHandler)
        self.server.effectController = self.effectController
        self.server.rgbStripController = self.rgbStripController
        self.server.serve_forever()
        print("ThreadedUDPServer stopped")

    def stop(self):
        self.udpClientGuardian.stop()
        self.server.shutdown()

    # check last pings from clients, responds with pong and remove clients
    # when there is no answer after 2 seconds
    class UDPClientGuardian(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self,name="UDPClientGuardian")
            self.stopped = False

        def run(self):
            while not self.stopped:
                for key in list(UDPClients.keys()):
                    if UDPClients[key].lastping + 2 < time():
                        print("ping missing, last ping: ",UDPClients[key].lastping," now is: ",time())
                        UDPClients[key].handleClose()
                        del UDPClients[key]
                sleep(0.5)

        def stop(self):
            self.stopped = True


CLIENT_TYPE_CONTROLLER = 0
CLIENT_TYPE_STRIPE = 1
CLIENT_TYPE_RECORDER = 2

UDPClients = {}


class UDPStripHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # print(self.client_address)
        if self.client_address not in UDPClients:
            UDPClients[self.client_address] = UDPClient(
                self.client_address, self.server.effectController, self.server.rgbStripController)
        UDPClients[self.client_address].handle(self.request)


class UDPClient():
    def __init__(self, client_address, effectController, rgbStripController):
        self.client_type = None
        self.rgbStrip = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_address = client_address
        self.effectController = effectController
        self.rgbStripController = rgbStripController
        self.sendToClientLock = False
        self.registered = False
        self.lastping = time()

    def handle(self, request):

        clientdata = request[0].decode()
        self.socket = request[1]
        #print(time(),"{} wrote:".format(self.client_address))
        #print(time(),"clientdata -> ", clientdata)
        # socket.sendto(bytes("pong","utf-8"),self.client_address)

        # Client Types:
        # CLIENT_TYPE_CONTROLLER = 0
        # CLIENT_TYPE_STRIPE = 1
        # CLIENT_TYPE_RECORDER = 2

        # UDP Registrierung Stripe: (nosend definiert, dass der stripe sich seine daten selbst anfordert)
        # r:1:NUM_LEDS[:nosend]
        # UDP Stripe sendet ping, woran festgemacht wird, ob er nocht lebt
        # s:ping
        # UDP 

        try:
            data = clientdata.split(':')
            #print(data)
            # r:1:srg strip name
            if data[0] == "r" and int(data[1]) == CLIENT_TYPE_STRIPE and data[2] != None and self.registered is False:
                self.registered = True
                self.client_type = CLIENT_TYPE_STRIPE
                # registers the strip with websocket object and name. the onRGBStripValueUpdate(rgbStrip) is called by
                # by the rgbStrip when an effectThread updates it
                # the self.rgbStrip variable is used to unregister the strip only

                ledcount = 1
                if data[3] != None:
                    ledcount = int(data[3])

                self.rgbStrip = self.rgbStripController.registerRGBStrip(
                    data[2], self.onRGBStripValueUpdate, ledcount)
            # s:ping
            if data[0] == "s" and data[1] == "ping":
                # if we got a ping and the client has no client type defined, send status unregistered, so the client knows that he has to register
                if self.client_type is None and self.socket is not None:
                    self.sendToClient('sr')
                self.lastping = time()
        except Exception as e:
            print(e, traceback.format_exc())

    # unregister the onChangeHandler
    # for now this function is not called when a client times out,
    # so they don't get unregistered. i mean there is no function that
    # is called when a client times out.

    def handleClose(self):
        if self.client_type is CLIENT_TYPE_STRIPE:
            self.rgbStripController.unregisterRGBStrip(self.rgbStrip)
        print(self.client_address, 'closed')

    # when a rgbStrip value is changed, send not json data but a formated string to client
    # d:[id off the LED, always 0 on RGB strips]:[red value 0-255]:[green value 0-255]:[blue value 0-255]
    def onRGBStripValueUpdate(self, rgbStrip):
        respdata = "d"
        tmplen = 0
        for i in range(rgbStrip.STRIP_LENGHT):
            if tmplen is 49:
                self.sendToClient(respdata)
                respdata = "d"
                tmplen = 0
            respdata = respdata + "{0:03}".format(i) + "{0:03}".format(rgbStrip.red[i]) + "{0:03}".format(rgbStrip.green[i]) + "{0:03}".format(rgbStrip.blue[i])
            tmplen = tmplen+1
        self.sendToClient(respdata)
        self.sendToClient('su')

    def sendToClient(self, message):
        #print("SendToClient:",self.client_address, message)
        self.socket.sendto(
            message.encode(), self.client_address
        )
