import json

from rgbUtils import effectControllerJsonHandler
from rgbUtils import rgbStripControllerJsonHandler
from webserver.SimpleWebSocketServer import WebSocket

import traceback
import logging


CLIENT_TYPE_CONTROLLER = 0
CLIENT_TYPE_STRIPE = 1
CLIENT_TYPE_RECORDER = 2


#class WebSocketError(Exception):
#    pass


class HTTPWebSocketsHandler(WebSocket):

    def __init__(self, effectController, rgbStripController, *args, **kwargs):
        self.effectController = effectController
        self.rgbStripController = rgbStripController
        self.client_type = CLIENT_TYPE_CONTROLLER
        self.rgbStrip = None
        super().__init__(*args, **kwargs)

    def handleMessage(self):
        try:
            print(self.address, self.data)
            data = json.loads(self.data)
            # Client Registration on the Websocket Server
            # maybe it would be better to use a websocket server thread for each client type,
            # can be done in future if there is too much latency
            if "register_client_type" in data:
                # the controler type, add handler on RGBStripContoller and send the current state of the controller
                if int(data['register_client_type']) is CLIENT_TYPE_CONTROLLER:
                    self.client_type = CLIENT_TYPE_CONTROLLER
                    # add effectController onControllerChangeHandler to get changes in the effectController eg start/stop effects, parameter updates, moved strips
                    # register rgbStripController onRGBStripRegistered/UnRegistered handler to get noticed about new rgbStrips is not necessary
                    # since we will get noticed from the effectController when it added the rgbStrip to the offEffect 
                    self.effectController.addOnControllerChangeHandler(self.onChange)
                # register new Stripes
                elif int(data['register_client_type']) is CLIENT_TYPE_STRIPE and "client_name" in data:
                    self.client_type = CLIENT_TYPE_STRIPE
                    # registers the strip with websocket object and name. the onRGBStripValueUpdate(rgbStrip) is called by 
                    # by the rgbStrip when an effectThread updates it
                    # the self.rgbStrip variable is used to unregister the strip only
                    self.rgbStrip = self.rgbStripController.registerRGBStrip(data["client_name"],self.onRGBStripValueUpdate)
                # register new Audio Recorders
                elif int(data['register_client_type']) is CLIENT_TYPE_RECORDER:
                    self.client_type = CLIENT_TYPE_RECORDER

            # controller responses are handled by the effectControllerJsonHandler
            if self.client_type is CLIENT_TYPE_CONTROLLER:
                response = effectControllerJsonHandler.responseHandler(self.effectController, self.rgbStripController, data)
                self.sendMessage(
                    json.dumps({
                        'response': response
                    })
                )
                return
            # the stripe should usualy not send any data, i do not know why it should...
            elif self.client_type is CLIENT_TYPE_STRIPE:
                return
            # audio recorder responses are handled by the effectControllerJsonHandler
            elif self.client_type is CLIENT_TYPE_RECORDER:
                return
        except Exception as e:
            print(e, traceback.format_exc())

    # notice about connects in terminal, the client has to register itself, see handleMessage
    def handleConnected(self):
        print(self.address, 'connected')

    # unregister the onChangeHandler
    # for now this function is not called when a client times out,
    # so they don't get unregistered. i mean there is no function that
    # is called when a client times out.
    def handleClose(self):
        if self.client_type is CLIENT_TYPE_CONTROLLER:
            self.effectController.removeOnControllerChangeHandler(self.onChange)
        elif self.client_type is CLIENT_TYPE_STRIPE:
            self.rgbStripController.unregisterRGBStrip(self.rgbStrip)
        elif self.client_type is CLIENT_TYPE_RECORDER:
            pass
        print(self.address, 'closed')

    # called when there are changes that should be pushed to the client.
    # - the effectController: start / stop effects, move strip to effect, changing effect params 
    # - the rgbStripController: add/removing strips 
    #     -> CLIENT_TYPE_CONTROLLER
    def onChange(self):
        if self.client_type is CLIENT_TYPE_CONTROLLER:
            self.sendMessage(
                json.dumps({
                    'effects': effectControllerJsonHandler.getEffects(self.effectController),
                    'rgbStrips': rgbStripControllerJsonHandler.getRGBStrips(self.rgbStripController),
                    'effectThreads': effectControllerJsonHandler.getEffectThreads(self.effectController)
                })
            )
            return
        elif self.client_type is CLIENT_TYPE_STRIPE:
            return
        elif self.client_type is CLIENT_TYPE_RECORDER:
            return

    # when a rgbStrip value is changed, send json data to client
    def onRGBStripValueUpdate(self,rgbStrip):
        self.sendMessage(
            json.dumps({
                'data': rgbStripControllerJsonHandler.getRGBData(rgbStrip)
            })
        )
