from rgbUtils.debug import debug
import uuid

class RGBStrip:
    # name = the name off the the strip, defined by the client connecting to the server
    # uid = unique id, if the strip sends one, use this (later maybe, or never, whatever)
    # lenght = the lenght off the strip, for future use of eg WS2812b strips, will be 1 by default
    def __init__(self,name,onValuesUpdateHandler,lenght=1):
        # UID should be updateable later, or not?
        # when updating, be sure it does not exist
        self.STRIP_UID = str(uuid.uuid4())
        self.STRIP_NAME = name
        self.STRIP_LENGHT = lenght

        self.onValuesUpdateHandler = onValuesUpdateHandler

        self.red = [0]*self.STRIP_LENGHT
        self.green = [0]*self.STRIP_LENGHT
        self.blue = [0]*self.STRIP_LENGHT
    
    def RGB(self,red,green,blue,brightness = 100):
        
        if(red < 0):
            red = 0
        if(red > 255):
            red = 255
        
        if(green < 0):
            green = 0
        if(green > 255):
            green = 255
        
        if(blue < 0):
            blue = 0
        if(blue > 255):
            blue = 255
        
        if(brightness < 0):
            brightness = 0
        if(brightness > 100):
            brightness = 100
            
        for x in range(self.STRIP_LENGHT):
            self.red[x] = int(red/100*brightness)
            self.green[x] = int(green/100*brightness)
            self.blue[x] = int(blue/100*brightness)
        
        self.onValuesUpdateHandler(self)
        
    def WS2812b(self,id,red,green,blue,brightness=100):
        if id < 0 and id > self.STRIP_LENGHT:
            print(self.STRIP_NAME," is max ",self.STRIP_LENGHT," Pixels long!")
            return
        else:
            if(red < 0):
                red = 0
            if(red > 255):
                red = 255
            
            if(green < 0):
                green = 0
            if(green > 255):
                green = 255
            
            if(blue < 0):
                blue = 0
            if(blue > 255):
                blue = 255
            
            if(brightness < 0):
                brightness = 0
            if(brightness > 100):
                brightness = 100
                
            self.red[id] = int(red/100*brightness)
            self.green[id] = int(green/100*brightness)
            self.blue[id] = int(blue/100*brightness)

        self.onValuesUpdateHandler(self,id)
            
    
    def off(self):
        for x in range(self.STRIP_LENGHT):
            self.red[x] = 0
            self.green[x] = 0
            self.blue[x] = 0
        
        self.onValuesUpdateHandler(self)

    def getData(self):
        self.hasNewData = False
        return [self.red,self.green,self.blue]



