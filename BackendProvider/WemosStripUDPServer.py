import threading
import socketserver
import socket
import traceback
from time import sleep, time
import json
import struct

class ThreadedUDPServer(threading.Thread):
    def __init__(self,effectController,rgbStripController):
        threading.Thread.__init__(self)
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
            threading.Thread.__init__(self)
            self.stopped = False

        def run(self):
            while not self.stopped:
                for key in list(UDPClients.keys()):
                    if UDPClients[key].lastping + 2 < time():
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
        #print(self.client_address)
        if self.client_address not in UDPClients:
            UDPClients[self.client_address] = UDPClient(self.client_address,self.server.effectController,self.server.rgbStripController)
        UDPClients[self.client_address].handle(self.request)
                
class UDPClient():
    def __init__(self,client_address,effectController,rgbStripController):
        self.client_type = None
        self.rgbStrip = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_address = client_address
        self.effectController = effectController
        self.rgbStripController = rgbStripController
        self.sendToClientLock = False
        self.lastping = time()

    def handle(self,request):

        clientdata = request[0].decode()
        self.socket = request[1]
        #print(time(),"{} wrote:".format(self.client_address))
        #print(time(),"clientdata -> ", clientdata)
        # socket.sendto(bytes("pong","utf-8"),self.client_address)

        try:
            data = clientdata.split(':')
            #print(data)
            #r:1:srg strip name
            if data[0] == "r" and int(data[1]) == CLIENT_TYPE_STRIPE and data[2] != None:
                    self.client_type = CLIENT_TYPE_STRIPE
                    # registers the strip with websocket object and name. the onRGBStripValueUpdate(rgbStrip) is called by 
                    # by the rgbStrip when an effectThread updates it
                    # the self.rgbStrip variable is used to unregister the strip only
                    self.rgbStrip = self.rgbStripController.registerRGBStrip(data[2],self.onRGBStripValueUpdate)
            #s:ping
            if data[0] == "s" and data[1] == "ping":
                # if we got a ping and the client has no client type defined, send status unregistered, so the client knows that he has to register
                if self.client_type is None and self.socket is not None:
                    self.sendToClient('s:unregistered')
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
        #print(self.client_address, 'closed')

    # when a rgbStrip value is changed, send json data to client
    def onRGBStripValueUpdate(self,rgbStrip,led = 0):
        self.sendToClient('d:'+str(led)+':'+str(rgbStrip.red[led])+':'+str(rgbStrip.green[led])+':'+str(rgbStrip.blue[led])+'')
            

    def sendToClient(self,message):
        while self.sendToClientLock is True:
            sleep(1)
        self.sendToClientLock = True
        if self.socket is not None:
            self.socket.sendto(
                message.encode(), self.client_address
            )
        self.sendToClientLock = False

# class UDPStripHandler:

#     def __init__(self):
#         #the rgbStrip object returned by the 
#         self.rgbStrip = None
#         # last ping command from the client
#         self.lastPing = 0


#     def handleMessage(self):
#         try:
#             print(self.address, self.data)
#             data = json.loads(self.data)
#             # Client Registration on the Websocket Server
#             # maybe it would be better to use a websocket server thread for each client type,
#             # can be done in future if there is too much latency
#             if "register_client_type" in data:
#                 # the controler type, add handler on RGBStripContoller and send the current state of the controller
#                 if int(data['register_client_type']) is CLIENT_TYPE_CONTROLLER:
#                     self.client_type = CLIENT_TYPE_CONTROLLER
#                     # add effectController onControllerChangeHandler to get changes in the effectController eg start/stop effects, parameter updates, moved strips
#                     # register rgbStripController onRGBStripRegistered/UnRegistered handler to get noticed about new rgbStrips is not necessary
#                     # since we will get noticed from the effectController when it added the rgbStrip to the offEffect 
#                     self.effectController.addOnControllerChangeHandler(self.onChange)
#                 # register new Stripes
#                 elif int(data['register_client_type']) is CLIENT_TYPE_STRIPE and "client_name" in data:
#                     self.client_type = CLIENT_TYPE_STRIPE
#                     # registers the strip with websocket object and name. the onRGBStripValueUpdate(rgbStrip) is called by 
#                     # by the rgbStrip when an effectThread updates it
#                     # the self.rgbStrip variable is used to unregister the strip only
#                     self.rgbStrip = self.rgbStripController.registerRGBStrip(data["client_name"],self.onRGBStripValueUpdate)
#                 # register new Audio Recorders
#                 elif int(data['register_client_type']) is CLIENT_TYPE_RECORDER:
#                     self.client_type = CLIENT_TYPE_RECORDER

#             # controller responses are handled by the effectControllerJsonHandler
#             if self.client_type is CLIENT_TYPE_CONTROLLER:
#                 response = effectControllerJsonHandler.responseHandler(self.effectController, self.rgbStripController, data)
#                 self.sendMessage(
#                     json.dumps({
#                         'response': response
#                     })
#                 )
#                 return
#             # the stripe should usualy not send any data, i do not know why it should...
#             elif self.client_type is CLIENT_TYPE_STRIPE:
#                 return
#             # audio recorder responses are handled by the effectControllerJsonHandler
#             elif self.client_type is CLIENT_TYPE_RECORDER:
#                 return
#         except Exception as e:
#             print(e, traceback.format_exc())

    

        