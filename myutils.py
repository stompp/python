import threading
import random

def rgb_to_hex(rgb,maximizeTo255 = False,init_format = "#"):
    r = rgb
    if maximizeTo255:

        # print(f"before maximize : {rgb}")
        m = float(max(rgb))
        if m > 0:
            m = 255.0/m
            # print(f"max is {m}")
            # r = (int(rgb[0]*m),int(rgb[1]*m),int(rgb[2]*m))
            r = map(lambda x: int(x*m), rgb)
            # print(f"r is {r}")
     
        # print(f"After maximize : {r}")
    format_str = init_format + len(r)*"%02x"
    return format_str % r
    # if(len(r) == 4):
    #     return '#%02x%02x%02x' % r       
    # return '#%02x%02x%02x' % rgb

# def argb_to_hex(rgb,maximizeTo255 = False):

def createRandomRGB(maxC = 255):
    o = (random.randint(0,maxC),random.randint(0,maxC),random.randint(0,maxC))
    return o

def mapValue(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
def constrainValue(x,out_min,out_max):
    return min(max(out_min,x),out_max)

class LoopThreadHelper():
    def __init__(self,method = 0):
        self.active = False
        self.started = False
        self.method = method
        self.thr = 0

    def loop(self):
        
        
        self.started = True
        try:
            while self.active == True:
                self.method()
        except:
            print("Thread method error")
            self.active = False
        print("Loop Thread finished")
        self.started = False
     

    def start(self):
        
        try:
            self.active = True
            # self.started = True
            self.thr = threading.Thread(target=self.loop)
            self.thr.daemon = True
            self.thr.start()
        except:
            print("Thread start error")
            self.active = False
            self.started = False
            
    
    def stop(self):
        self.active = False
        

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


class TransceiverHelper():
    def __init__(self):

        self.is_connected = False
      
        self.time_out = 5
        self.start_marker = ""
        self.end_marker = ""
        self.connection_succes_msg = "{!!}"
        self.line_adjustment = "\n"
        self.last_msg = ""

        self.on_msg_received = MessageBroadcaster()
        self.on_msg_received.add(self.printInput)
     

        self.input_loop = LoopThreadHelper()
        self.input_loop.method = self.readInputLoop



        self.on_msg_sent = MessageBroadcaster()

        self.info_broadcaster = MessageBroadcaster()
        self.info_broadcaster.add(self.debug)
        
    def debug(self,msg):
        print(msg)

    def printInput(self,msg):
        print(msg) 

    def format_msg(self,msg):
        return self.start_marker + msg + self.end_marker + self.line_adjustment

    def sendStr(self,str):
        pass
                

    def readLine(self,doStrip = True):
        pass
    
        


    def readInputLoop(self):
        pass
       
    

    def waitForRawMessage(self, expected):
        pass
      

    def getConnectionReadyMessage(self):
        pass
        
        
    def connect(self):
        pass
       

    def disconnect(self):
        pass
        

   

