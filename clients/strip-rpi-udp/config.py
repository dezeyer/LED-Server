from util.RGBStrip import RGBStrip as RGBStrip

#use the BCM pin numbers here
rgbStrips = [
    #RGBStrip("Test Dahem", 4, 17 , 22),
    RGBStrip("Unter Theke", 20, 16 , 21),
    RGBStrip("Über Theke", 22, 13, 27),
    RGBStrip("Fensterbank", 5, 26, 6)
]
# set remote address and port
remoteaddr = ("192.168.0.255",8002)