# simple inquiry example
import bluetooth
from myutils import *
import time

class BluetoothSocketHelper(TransceiverHelper):
    def __init__(self):
        super(BluetoothSocketHelper,self).__init__()
        self.is_connected = False
        self.address = ""
        self.port = 1
        self.socket = bluetooth.BluetoothSocket()
        self.socket.settimeout(0.001)
        self.socket.setblocking(False)
        self.on_msg_received.add(self.printInput)
        
        self.buff = ""
    
      
    def sendStr(self,str):

        if self.is_connected:
            try:
                # self.socket.send(str.encode())
                msg = self.format_msg(str)
                self.socket.sendall(msg.encode())
                self.on_msg_sent.broadcast(msg)
            except:
                self.info_broadcaster.broadcast("Send Error")
                

    def read(self, elements = 1):
        x = ""
        if self.is_connected:
            data = self.socket.recv(elements)
            # x = data.decode('utf-8').strip()
            x = data.decode('utf-8').rstrip("\r\n")

            if len(x):
                return x
            #     print(f"x is {x} len x is {len(x)}")
            # else :
            #     print("x is empty")
               
        return x

    def readLines(self):

        data = self.socket.recv(1024)
        
        if len(data) > 0:

            self.buff += data.decode()
            
            lines = self.buff.splitlines()
            if not self.buff.endswith("\n"):
               
                self.buff = lines.pop()
            for line in lines:
                line.rstrip("\r")
                yield line

          
            



    # def readLine(self,doStrip = True):

       
    #     doIt = True
    #     msg = ""

    #     while doIt == True:
    #         x = self.read(1)
    #         if x and len(x) > 0:
               
    #             msg += x

    #         if msg.endswith('\n'):
    #             break
    #         else:
    #             doIt = False
    #             break
        
    #     if doStrip:
    #         msg = msg.rstrip("\r\n")      
        
    #     # print(f"read msg is {msg}")
    #     return msg
      
      


    def readInputLoop(self):
        
        try:
            for msg in self.readLines():
                if len(msg) > 0 :
                # print("readInputLoop -> Broadcasting ")
                    self.on_msg_received.broadcast(msg)
            # msg = self.readLine()
            # if len(msg) > 0 :
            #     # print("readInputLoop -> Broadcasting ")
            #     self.on_msg_received.broadcast(msg)
        except:
             self.info_broadcaster.broadcast(self.__class__ + " readInputLoop Error")
    

    def waitForRawMessage(self, expected):
        pass
        # msg = ""
        # t = time.time()
        # ok = False
        # end_time = t+self.time_out
        
        # while (ok == False) and (time.time() <= end_time):
            
        #     if self.inWaiting() > 0 :
        #         x = self.read().decode('utf-8')
        #         msg += x

        #     if msg == expected :
        #         self.on_msg_received.broadcast(msg)
        #         print("elapsed time is " + str(time.time()- t))
        #         ok = True

        # self.last_msg = msg
    
        # return ok


    def getConnectionReadyMessage(self):
        pass
        # if len(self.connection_succes_msg):

        #     return self.waitForRawMessage(self.connection_succes_msg)
        # return self.is_open
        
    def connect(self):

        if(self.is_connected) :
            return self.is_connected

        self.is_connected = False

        try:
            self.socket.connect((self.address,self.port))

            self.is_connected = True
            self.info_broadcaster.broadcast("Connected")
            self.input_loop.start()

        except:
            self.info_broadcaster.broadcast("Connection error")
          
        return self.is_connected

       
        # ok = False

        # try:
        #     self.open()
        #     try:
        #         self.info_broadcaster.broadcast("SERIAL CONNECTED, WAITING FOR READY MESSAGE")
        #         # print("SERIAL CONNECTED, WAITING FOR READY MESSAGE")
        #         if self.is_open and len(self.connection_succes_msg) > 0:
        #             if self.getConnectionReadyMessage() :
        #                 self.info_broadcaster.broadcast("GOT WELCOME MESSAGE")
        #                 ok = True        
        #             else:
        #                 self.info_broadcaster.broadcast("CLOSING, WRONG WELCOME MESSAGE RECEIVED :" + self.last_msg)
        #                 if self.is_open:
        #                     self.close()                                             
        #         elif self.is_open:
        #             ok = True
                    
        #         if ok:
        #             self.info_broadcaster.broadcast("CONNECTED")
        #             self.input_loop.start()

            
        #     except:
        #         self.info_broadcaster.broadcast("CONNECTION ERROR")
        #         # print("CONNECTION ERROR")
                
        # except:
        #     self.info_broadcaster.broadcast("SERIAL NOT AVAILABLE")
        #     # print ("SERIAL NOT AVAILABLE")
        
        # if ok == False and self.is_open:
        #     try:
        #         self.close()
        #     except: 
        #         pass
        # return ok

    def disconnect(self):

        try :
            self.input_loop.stop()
            self.is_connected = False
            self.socket.close()
        except:
            self.info_broadcaster.broadcast("Disconnect Error") 
      
    def printDebug(self,msg):   
       print(msg)
