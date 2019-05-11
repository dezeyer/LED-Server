from Util.PyAudioRecorder import PyAudioRecorder
from random import randint
import time
import socket
import pickle

remoteaddr = ("0.0.0.0",8002)

# PyAudioRecorder uses the default 
pyAudioRecorder: PyAudioRecorder = PyAudioRecorder()
#pyAudioRecorder.start()
print(pyAudioRecorder.p.get_default_input_device_info())
lastping = time.time()-1
lastupdate = time.time()-1
localaddr = ("",randint(6000,7000))

udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udpsocket.settimeout(.002)

registered:bool = False

while True:
    #print(time.time() - self.lastping)
    if time.time() - lastping > .5 :
        udpsocket.sendto("s:ping".encode(), remoteaddr)
        lastping = time.time()
    ftt = pyAudioRecorder.fft()
    #print(ftt)


    if time.time() - lastupdate > 0.00833333333 and registered:
    #if pyAudioRecorder.has_new_audio:
        # there must be a better solution to do this.
        # this looks like my silly arduino code, but it works
        values: str = "d:xs"
        i = 0
        j = 0
        udpsocket.sendto(("dlen:"+str(len(ftt[0]))+":"+str(len(ftt[1]))+"").encode(), remoteaddr)
        for value in ftt[0]:
            values = values+":"+str(j)+"|"+str(value)
            i = i+1
            j = j+1
            if i == 20:
                udpsocket.sendto(values.encode(), remoteaddr)
                i = 0
                values= "d:xs"

        
        values = "d:ys"
        i = 0
        j = 0
        for value in ftt[1]:
            values = values+":"+str(j)+"|"+str(value)
            i = i+1
            j = j+1
            if i == 20:
                udpsocket.sendto(values.encode(), remoteaddr)
                i = 0
                values= "d:ys"
        

        udpsocket.sendto("d:c".encode(), remoteaddr)
        lastupdate = time.time()
    
    try:
        rbytes, address = udpsocket.recvfrom(4096)
        remoteaddr = address
        data = rbytes.decode('UTF-8')
        if data:
            if data[0] is "s" and data[1] is "r":
                registered = True
                udpsocket.sendto(("r:2:"+pyAudioRecorder.p.get_default_input_device_info()['name']+"").encode(), address)
    except socket.timeout:
        pass
        
