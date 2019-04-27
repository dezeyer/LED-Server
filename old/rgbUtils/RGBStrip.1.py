try:
    import RPi.GPIO as GPIO
except ImportError:
    import rgbUtils.fakeGPIO as GPIO
from rgbUtils.debug import debug
class RGBStrip:
    STRIP_NAME = None

    issetup = False

    effectClassInstance = None
    
    # GPIO PWM Frequenz
    hertz = 100 

    RED_PIN = None
    GREEN_PIN = None
    BLUE_PIN = None

    RED_PWM = None
    GREEN_PWM = None
    BLUE_PWM = None


    def __init__(self,STRIP_NAME,RED_PIN,GREEN_PIN,BLUE_PIN):
        self.STRIP_NAME = STRIP_NAME
        self.RED_PIN = RED_PIN
        self.GREEN_PIN = GREEN_PIN
        self.BLUE_PIN = BLUE_PIN

    def init(self):
        if not self.issetup:
            debug("setting up")
            # setup RED
            GPIO.setup(self.RED_PIN, GPIO.OUT)
            self.RED_PWM = GPIO.PWM(self.RED_PIN, self.hertz)
            self.RED_PWM.start(0)
            # setup GREEN
            GPIO.setup(self.GREEN_PIN, GPIO.OUT)
            self.GREEN_PWM = GPIO.PWM(self.GREEN_PIN, self.hertz)
            self.GREEN_PWM.start(0)
            # setup BLUE
            GPIO.setup(self.BLUE_PIN, GPIO.OUT)
            self.BLUE_PWM = GPIO.PWM(self.BLUE_PIN, self.hertz)
            self.BLUE_PWM.start(0)

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
        
        if(brightness < 0):
            brightness = 0
        if(brightness > 100):
            brightness = 100
            
        self.red = red
        self.green = green
        self.blue = blue
        self.RED_PWM.ChangeDutyCycle(round((red/255*100)/100*brightness,2))
        self.GREEN_PWM.ChangeDutyCycle(round((green/255*100)/100*brightness,2))
        self.BLUE_PWM.ChangeDutyCycle(round((blue/255*100)/100*brightness,2))
    
    def stop(self):
        self.RED_PWM.ChangeDutyCycle(0)
        self.GREEN_PWM.ChangeDutyCycle(0)
        self.BLUE_PWM.ChangeDutyCycle(0)
        self.RED_PWM.stop()
        self.GREEN_PWM.stop()
        self.BLUE_PWM.stop()



    # I have to be sure that a rgbStip is only used by one Effect at once, so i save the current running Effect Class Object
    # in the rgbStip object.
    def setEffectClassInstance(self,effectClass):
        debug("RGBStrip "+ self.STRIP_NAME + " Effect is now " + str(effectClass))
        self.effectClassInstance = effectClass

    def getEffectClassInstance(self):
        return self.effectClassInstance



