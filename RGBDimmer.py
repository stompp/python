from random import randint
from myutils import *
from kelving2rgb import *
class RGBDimmerController():
    MIN_TEMPERATURE = 1000
    MAX_TEMPERATURE = 12000
    MIN_HUE = 0
    MAX_HUE = 359
    MIN_BRIGHTNESS = 0
    MAX_BRIGHTNESS = 255
    MIN_SATURATION = 0
    MAX_SATURATION = 255
    MIN_COMPONENT = 0
    MAX_COMPONENT = 255

    def __init__(self):
        self.senders = MessageBroadcaster()

    def send(self,msg):
        self.senders.broadcast(msg)

    def sendCommand(self,command):
        self.send(f"C{command}")

    def setRGB(self,r,g = 0,b = 0):
        str = "R{},{},{}"
        if(type(r) == tuple):
            self.send(str.format(r[0],r[1],r[2]))
        else:
            self.send(str.format(r,g,b))

    def setRandomRGB(self):
        self.setRGB(createRandomRGB())

    def setTemperature(self,temperature):
        self.send("K {}".format(int(temperature)))

    def setHue(self,hue):
        if hue >= self.MIN_HUE and hue < self.MAX_HUE:
            self.send("H {}".format(int(hue))) 
    def setTone(self,tone):
        self.send("T {}".format(int(tone)))

    def setRandomHue(self):
        h = randint(self.MIN_HUE,2*self.MAX_HUE)%self.MAX_HUE
        self.setTone(h)
    
    def setRandomTemperature(self):
        t = randint(self.MIN_TEMPERATURE,self.MAX_TEMPERATURE)
        self.setTone(t)

    def setRandomTone(self):
        t = randint(0,2000)
        if t > 1500:
            self.setRandomTemperature()
        else :
            self.setRandomHue()
    


   

    def setBrightness(self,brightness):
        if brightness >= self.MIN_BRIGHTNESS and brightness <= self.MAX_BRIGHTNESS:
            self.send("B {}".format(int(brightness)))

