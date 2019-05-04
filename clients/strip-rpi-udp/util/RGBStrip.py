try:
    import RPi.GPIO as GPIO
    demo = False
except ImportError:
    print("!!! Install RPi.GPIO, running demo !!!")
    demo = True
# setup PRi.GPIO
if not demo:
    GPIO.setmode(GPIO.BCM)

class RGBStrip:
    STRIP_NAME = None
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

        if not demo:
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

    def RGB(self,red,green,blue,brightness = 100):
        if demo:
            print(self.STRIP_NAME,red,green,blue)
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
            self.RED_PWM.ChangeDutyCycle(round(red/255*100,2))
            self.GREEN_PWM.ChangeDutyCycle(round(green/255*100,2))
            self.BLUE_PWM.ChangeDutyCycle(round(blue/255*100,2))

    def stop(self):
        if not demo:
            self.RED_PWM.ChangeDutyCycle(0)
            self.GREEN_PWM.ChangeDutyCycle(0)
            self.BLUE_PWM.ChangeDutyCycle(0)
            self.RED_PWM.stop()
            self.GREEN_PWM.stop()
            self.BLUE_PWM.stop()