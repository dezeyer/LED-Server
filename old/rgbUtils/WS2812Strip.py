from rgbUtils.debug import debug
from rgbUtils.RGBStrip import RGBStrip

# The WS2812Strip must have the same behavior as the 12v rgb strip,
# plus some extras for these type of strips only.
# A WS1812 Strip can be initialised as multiple RGB Strips by defining 
# the start and the end led's. lets's see how that goes
class WS2812Strip(RGBStrip):
    STRIP_NAME = None
    
    master = None
    FIRST_LED = None
    LAST_LED = None

    def __init__(self,STRIP_NAME,FIRST_LED,LAST_LED,WS2812B_MASTER_STRIP):
        self.STRIP_NAME = STRIP_NAME
        self.master = WS2812B_MASTER_STRIP
        self.FIRST_LED = FIRST_LED
        self.LAST_LED = LAST_LED
    
    # init the WS2812 part. since the master sets all pixel to 0 in init,
    # we have nothing to do here.
    def init(self):
        if not self.issetup:
            debug("setting up")
            self.issetup = True
    
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
            green = 255
        
        if(brightness < 0):
            brightness = 0
        if(brightness > 255):
            brightness = 100

        self.red = red
        self.green = green
        self.blue = blue
        self.master.setPixelColorRange(self.FIRST_LED,self.LAST_LED, int(round(red/100*brightness)), int(round(green/100*brightness)), int(round(blue/100*brightness)))
        
    
    def stop(self):
        self.master.setPixelColorRange(self.FIRST_LED,self.LAST_LED, 0, 0,0)



