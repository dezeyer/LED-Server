from random import randint
import time
import socket

class UDPListner:
    lastping = time.time()-1

    def __init__(self, rgbStrip, remoteaddr):
        self.rgbStrip = rgbStrip
        self.remoteaddr = remoteaddr
        self.localaddr = ("",randint(6000,7000))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(.002)

    def loop(self):
        #print(time.time() - self.lastping)
        if time.time() - self.lastping > .5 :
            self.socket.sendto("s:ping".encode(), self.remoteaddr)
            self.lastping = time.time()
        try:
            data, address = self.socket.recvfrom(4096)
            data = data.decode('UTF-8')
            #print(data[0],data[1])
            if data:
                if data[0] is "s" and data[1] is "r":
                    self.socket.sendto(("r:1:"+self.rgbStrip.STRIP_NAME+":1").encode(), address)
                if data[0] is "d":
                    self.rgbStrip.RGB(self.getRgbVal(data,1),self.getRgbVal(data,4),self.getRgbVal(data,7))
        except socket.timeout:
            pass

    def getRgbVal(self,data,pos):
        return 100*int(data[pos]) + 10*int(data[pos+1]) + int(data[pos+2]) 