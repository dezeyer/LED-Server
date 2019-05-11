#!/usr/bin/python
import os
import sys
import time
import traceback
import signal


def main():
    try:
        running: bool = True
        if(os.path.dirname(sys.argv[0]) is not ""):
            os.chdir(os.path.dirname(sys.argv[0]))

        # i want some external providers the effects can interact with. for example the music reaction.
        # Idea is: eg a Pi with a soundcard processing input via pyaudio and sending this data to the server. an musicEffect is bind to this input and processing it.
        # to be as flexible as possible the client registers with a name(sting), a type(string) and the data as an dict. the effect filters these clients by type. jea?

        
        from Utils.RGBStripController import RGBStripController
        rgbStripController: RGBStripController = RGBStripController()

        #signal.signal(signal.SIGINT, rgbStripController.stop())
        #signal.signal(signal.SIGTERM, rgbStripController.stop())

        
        from Utils.EffectController import EffectController
        effectController: EffectController = EffectController(rgbStripController)

        #signal.signal(signal.SIGINT, effectController.stopAll())
        #signal.signal(signal.SIGTERM, effectController.stopAll())

        # register effectControllers onRGBStripRegistered and onRGBStripUnregistered handler on the rgbStripContoller to detect added or removed strips
        rgbStripController.addOnRGBStripRegisteredHandler(
            effectController.onRGBStripRegistered
        )
        rgbStripController.addOnRGBStripUnRegisteredHandler(
            effectController.onRGBStripUnRegistered
        )

        # this is a "Backend Provider" that interacts with the effectController and also the rgbStripContoller (via effectController)
        # this could be seperated in one websocket server for the frontend and one for the rgbStrips
        # or an other frontend / rgbStrip backend provider not using websockets. you could integrate alexa, phillips hue like lamps or whatever you like!
        # but then there must be some autoloading of modules in a folder like the effects for easy installing. //todo :)
        print("starting websocket:8001")
        import BackendProvider.WebSocketProvider as WebSocketProvider
        webSocketThread = WebSocketProvider.ThreadedWebSocketServer(
            effectController, rgbStripController)

        #signal.signal(signal.SIGINT, webSocketThread.stop())
        #signal.signal(signal.SIGTERM, webSocketThread.stop())

        print("starting UPDSocketProvider:8002")
        import BackendProvider.UDPSocketProvider as UPDSocketProvider
        udpSocketThread = UPDSocketProvider.ThreadedUDPServer(
            effectController, rgbStripController)

        #signal.signal(signal.SIGINT, udpSocketThread.stop())
        #signal.signal(signal.SIGTERM, udpSocketThread.stop())

        while running:
            time.sleep(1)

    except Exception as e:
        running = False
        print(e, traceback.format_exc()) 
    finally:
        print('shutting down the LED-Server')
        try:
            webSocketThread.stop()
        except:
            pass
        try:
            udpSocketThread.stop()
        except:
            pass
        try:
            effectController.stopAll()
        except:
            pass


if __name__ == '__main__':
    main()
