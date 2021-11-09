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

        self.on_msg_received.add(self.printInput)
        
        

    
      
    def sendStr(self,str):

        if self.is_connected:
            try:
                self.socket.send(str.encode())
                self.on_msg_sent.broadcast(str)
            except:
                self.info_broadcaster.broadcast("Send Error")
                

    def read(self):
        x = ""
        if self.is_connected:
            data = self.socket.recv(1)
          

            # x = data.decode('utf-8').strip()
            x = data.decode('utf-8').rstrip("\r\n")

            if len(x):
                return x
            #     print(f"x is {x} len x is {len(x)}")
            # else :
            #     print("x is empty")
               
        return ""



    def readLine(self,doStrip = True):

        doIt = True
        msg = ""

        while doIt == True:
            x = self.read()
            if x and len(x) > 0:
               
                msg += x
             
            else:
                doIt = False
                break
                
        
        # print(f"read msg is {msg}")
        return msg
        # m = ""
        # l = 1
        # ok = True
        # try:
        #     while True:
        #     # try:
        #         data = ""
        #         try:
        #             data = self.socket.recv(1)
        #         except:
        #             print("read data error data")

        #         if len(data) == 0:
        #             print("breaking")
        #             break

        #         else:
        #             x = ""
        #             try:
        #                 x = data.decode('utf-8')
        #             except:
        #                 x = ""
        #             print(f"x is {x}")

        #             if len(x) > 0:
        #                 print(f"lenx is {len(x)}")
        #                 m += x
        #                 print(f"msg is {m}")
        #             else:
                        
        #                 break
        #                 print(f"lenx is 0")
        #                 ok = False
                        
              
        #     # except:
        #     #     ok = False


         

                   
           
        # except:

        #     self.info_broadcaster.broadcast("Socket read error")
            
        # if len(m) :

        #     if(doStrip):
        #         m = m.rstrip("\r\n")

        # print(f"message to return{m}")        
        # return m

      


    def readInputLoop(self):
        
        try:
            msg = self.readLine()
            if len(msg) > 0 :
                # print("readInputLoop -> Broadcasting ")
                self.on_msg_received.broadcast(msg)
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
            # self.input_loop.stop()
            self.is_connected = False
            self.socket.close()
        except:
            self.info_broadcaster.broadcast("Disconnect Error") 
      
    def printDebug(self,msg):   
       print(msg)
