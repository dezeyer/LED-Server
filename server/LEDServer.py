#!/usr/bin/python
import os
import sys
import time
import traceback


def main():
    try:

        running = True
        if(os.path.dirname(sys.argv[0]) is not ""):
            os.chdir(os.path.dirname(sys.argv[0]))

        # i want some external providers the effects can interact with. for example the music reaction.
        # Idea is: eg a Pi with a soundcard processing input via pyaudio and sending this data to the server. an musicEffect is bind to this input and processing it.
        # to be as flexible as possible the client registers with a name(sting), a type(string) and the data as an dict. the effect filters these clients by type. jea?

        # rgbStrips register themselves at the rgbStripContoller
        # the rgbStripController calls the backend Provider's onChange function
        # when there are new values for the strip
        from rgbUtils.rgbStripController import rgbStripController
        rgbStripController = rgbStripController()
        rgbStripController.start()

        # the effectController handles the effects and pushes the values to the rgbStripContoller
        # it also calls the backendProvider's onChange function when there are changes made on the effects
        from rgbUtils.effectController import effectController
        effectController = effectController(rgbStripController)

        # register effectControllers onRGBStripRegistered and onRGBStripUnregistered handler on the rgbStripContoller to detect added or removed strips
        rgbStripController.addOnRGBStripRegisteredHandler(
            effectController.onRGBStripRegistered)
        rgbStripController.addOnRGBStripUnRegisteredHandler(
            effectController.onRGBStripUnRegistered)

        # this is a "Backend Provider" that interacts with the effectController and also the rgbStripContoller (via effectController)
        # this could be seperated in one websocket server for the frontend and one for the rgbStrips
        # or an other frontend / rgbStrip backend provider not using websockets. you could integrate alexa, phillips hue like lamps or whatever you like!
        # but then there must be some autoloading of modules in a folder like the effects for easy installing. //todo :)
        print("starting websocket:8001")
        import BackendProvider.WebSocketProvider as WebSocketProvider
        webSocketThread = WebSocketProvider.ThreadedWebSocketServer(
            effectController, rgbStripController)

        print("starting UPDSocketProvider:8002")
        import BackendProvider.UDPSocketProvider as UPDSocketProvider
        udpSocketThread = UPDSocketProvider.ThreadedUDPServer(
            effectController, rgbStripController)

        while running:
            time.sleep(1)

    except Exception as e:
        running = False
        print(e, traceback.format_exc())
    finally:
        print('shutting down the LED-Server')
        webSocketThread.stop()
        udpSocketThread.stop()
        effectController.stopAll()


if __name__ == '__main__':
    main()
