import serial
from serial import Serial
import time
from myutils import *


    

class SerialHelper(Serial):
    def __init__(self, *args, **kwargs):
        super(SerialHelper, self).__init__(*args, **kwargs)
      
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

    # def broadcastInputMsg(self,msg):
    #     try:
    #         if len(msg) > 0 :
    #             for m in self.on_msg_received_actions:
    #                 m(msg)
    #     except:
    #         print("SerialHelper: Error broadcasting input message ")

    # def broadcastSentMsg(self, msg):
    #     try:
    #         if len(msg) > 0 :
    #             for m in self.on_msg_sent_actions:
    #                 m(msg)
    #     except:
    #         print("SerialHelper: Error broadcasting sent message ")


    def sendStr(self,str):
        try:
            if self.is_open:
                msg = self.start_marker + str + self.end_marker + self.line_adjustment
                self.write(msg.encode())
                self.on_msg_sent.broadcast(msg)
        except:
            print("SerialHelper: Error sending str")

    def readLine(self,doStrip = True):

        try:       
            msg = ""

            if self.inWaiting() > 0:
                x = self.readline().decode('utf-8')
                if doStrip:
                    msg = x.rstrip("\r\n")
                else:   
                    msg = x

            return msg
        except:
            print("SerialHelper: Error reading line")


    def readInputLoop(self):
        try:
            msg = self.readLine()
            self.on_msg_received.broadcast(msg)
        except:
            print(self.__class__ + " readInputLoop Error")
    

    def waitForRawMessage(self, expected):
       
        msg = ""
        t = time.time()
        ok = False
        end_time = t+self.time_out
        
        while (ok == False) and (time.time() <= end_time):
            
            if self.inWaiting() > 0 :
                x = self.read().decode('utf-8')
                msg += x

            if msg == expected :
                self.on_msg_received.broadcast(msg)
                print("elapsed time is " + str(time.time()- t))
                ok = True

        self.last_msg = msg
    
        return ok


    def getConnectionReadyMessage(self):
       
        if len(self.connection_succes_msg):

            return self.waitForRawMessage(self.connection_succes_msg)
        return self.is_open
        
    def connect(self):

        ok = False

        try:
            self.open()
            try:
                self.info_broadcaster.broadcast("SERIAL CONNECTED, WAITING FOR READY MESSAGE")
                # print("SERIAL CONNECTED, WAITING FOR READY MESSAGE")
                if self.is_open and len(self.connection_succes_msg) > 0:
                    if self.getConnectionReadyMessage() :
                        self.info_broadcaster.broadcast("GOT WELCOME MESSAGE")
                        ok = True        
                    else:
                        self.info_broadcaster.broadcast("CLOSING, WRONG WELCOME MESSAGE RECEIVED :" + self.last_msg)
                        if self.is_open:
                            self.close()                                             
                elif self.is_open:
                    ok = True
                    
                if ok:
                    self.info_broadcaster.broadcast("CONNECTED")
                    self.input_loop.start()

            
            except:
                self.info_broadcaster.broadcast("CONNECTION ERROR")
                # print("CONNECTION ERROR")
                
        except:
            self.info_broadcaster.broadcast("SERIAL NOT AVAILABLE")
            # print ("SERIAL NOT AVAILABLE")
        
        if ok == False and self.is_open:
            try:
                self.close()
            except: 
                pass
        return ok

    def disconnect(self):
        if self.isOpen:
            self.input_loop.active = False
            self.close()

    def printDebug(self,msg):
        print(msg)



if __name__ == '__main__':
    s = SerialHelper()
    s.port = 'COM5'
    s.baudrate = 115200
    s.connect()
    while(True):
        continue