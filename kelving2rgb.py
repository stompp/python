from math import log, pow,ceil
from myutils import constrainValue,mapValue

class Kelvin2RGB():
    MIN_TEMPERATURE = 1000
    MAX_TEMPERATURE = 12000
    MIN_BRIGHTNESS = 0
    MAX_BRIGHTNESS = 100
    MIN_COMPONENT = 0
    MAX_COMPONENT = 255

    def __init__(self, temperature, brightness = MAX_BRIGHTNESS):
       
        self.temperature = int(constrainValue(temperature,self.MIN_TEMPERATURE,self.MAX_TEMPERATURE))
        self.brightness = int(ceil(constrainValue(brightness,self.MIN_BRIGHTNESS,self.MAX_BRIGHTNESS)))
        self.calc_rgb()

    def calc_rgb(self):
        self.calc_red()
        self.calc_green()
        self.calc_blue()

    def calc_red(self):
        self.red = 255.0
        temperature = self.temperature/self.MAX_BRIGHTNESS
        if temperature > 66.0 :
            self.red = temperature - 60.0
            self.red = 329.698727466 * pow(self.red,-0.1332047592)
        self.red = self.constrain_component(self.red)
        self.red = self.calc_component_brightness(self.red)
       
    def calc_green(self):
        self.green = 0.0
        temperature = self.temperature/self.MAX_BRIGHTNESS
        if temperature <= 66.0 :     
            self.green = (99.4708025861 * log(temperature)) - 161.1195681661
        else :
            self.green = 288.1221695283 * pow(temperature - 60.0, -0.0755148492)
        
        self.green = self.constrain_component(self.green)
        self.green = self.calc_component_brightness(self.green)
       
    def calc_blue(self):
        self.blue = 255.0
        temperature = self.temperature/self.MAX_BRIGHTNESS
        if temperature<65 :
            if temperature <= 19.0:
                self.blue = 0
            else:
                self.blue = (138.5177312231 * log(temperature - 10.0)) - 305.0447927307
           
        self.blue = self.constrain_component(self.blue)
        self.blue = self.calc_component_brightness(self.blue)

    def constrain_component(self,component):
        value = component
        if type(value) == type(float):
            value = int(value)
        return constrainValue(value,self.MIN_COMPONENT,self.MAX_COMPONENT)

    def calc_component_brightness(self,component):
        value = component
        if type(value) == type(float):
            value = int(value)
        return int( mapValue(self.brightness,self.MIN_BRIGHTNESS,self.MAX_BRIGHTNESS,self.MIN_COMPONENT,value))

    def rgb(self):
        rgb = [self.red,self.green,self.blue]
        return rgb

    def setTemperature(self, temperature):
        self.temperature = int(constrainValue(temperature,self.MIN_TEMPERATURE,self.MAX_TEMPERATURE))
        self.calc_rgb()

    def setBrightness(self, brightness):
        self.brightness = int(ceil(constrainValue(brightness,self.MIN_BRIGHTNESS,self.MAX_BRIGHTNESS)))
        self.calc_rgb()
    
    def set(self,temperature,brightness):
        self.temperature = int(constrainValue(temperature,self.MIN_TEMPERATURE,self.MAX_TEMPERATURE))
        self.brightness = int(ceil(constrainValue(brightness,self.MIN_BRIGHTNESS,self.MAX_BRIGHTNESS)))
        self.calc_rgb()

