import threading
import random

def createRandomRGB(maxC = 255):
    o = (random.randint(0,maxC),random.randint(0,maxC),random.randint(0,maxC))
    return o

def mapValue(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def constrainValue(x,out_min,out_max):
    return min(max(out_min,x),out_max)

class LoopThreadHelper():
    def __init__(self):
        self.active = False
        self.started = False
        self.method = 0
        self.thr = 0

    def loop(self):
        
        
        self.started = True
        try:
            while self.active:
                self.method()
        except:
            print("Thread method error")
        self.started = False
     

    def start(self):
        
        try:
            self.active = True
            self.started = True
            self.thr = threading.Thread(target=self.loop)
            self.thr.daemon = True
            self.thr.start()
        except:
            print("Thread start error")
            self.active = False
            self.started = False
    
    def __del__(self):
        self.active = False  
        while self.started:
            continue
      


class MethodsList():

    def __init__(self):

        self.methods = list()

    def add(self, m):
        if m not in self.methods:
            self.methods.append(m)
    
    def remove(self, m):
        if m in self.methods:
            self.methods.remove(m)

    def run(self, param):
        for m in self.methods:
            m(param)
            
    def __del__(self):
        self.methods.clear()
    

class MessageBroadcaster(MethodsList):
    def __init__(self):
        super(MessageBroadcaster,self).__init__()

    def broadcast(self, msg):
        if len(msg):
            self.run(msg)

    def __del__(self):
        return super().__del__()
