import serial
import time
import threading

port = 'COM3'
baud_rate = 9600
arduino = 0
time_out = 5

start_marker = ""
end_marker = ""
connection_succes_msg = "{!!!}"
last_msg = ""

def sendStr(str):
    global arduino
    arduino.write(str.encode())

def readLine(doStrip = True):
    global arduino
    
    msg = ""

    if arduino.inWaiting() > 0:
        x = arduino.readline().decode('utf-8')
        if doStrip:
            msg = x.rstrip("\r\n")
        else:   
            msg = x

    return msg

def waitForRawMessage(expected):
    global arduino, time_out,last_msg
    msg = ""
    t = time.time()
    ok = False
    end_time = t+time_out
      
    while (ok == False) and (time.time() <= end_time):
        
        if arduino.inWaiting() > 0 :
            x = arduino.read().decode('utf-8')
            msg += x

        if msg == expected :
            print("elapsed time is " + str(time.time()- t))
            ok = True

    last_msg = msg
 
    return ok


def getConnectionReadyMessage():
    global connection_succes_msg
    return waitForRawMessage(connection_succes_msg) if len(connection_succes_msg) else True
    
        


def connect():

    global arduino, port, baud_rate,last_msg

    ok = False

    try:
        arduino = serial.Serial(port,baud_rate)
        try:
            print("SERIAL CONNECTED, WAITING FOR READY MESSAGE")
            if getConnectionReadyMessage() :
                ok = True
                print("CONNECTED")
            else:
                arduino.close()
                print("RECEIVED :" + last_msg)
           
        except:
            
            print("CONNECTION ERROR")
            
    except:
        
        print ("SERIAL NOT AVAILABLE")
    
    return ok
   
print_input_thread_active = False
print_input_thread_started = False 

# def printInput():

#     while True:
#         msg = readLine()
#         while len(msg) > 0:
#             print(msg)
#             msg = readLine()

def printInputThread():
    global print_input_thread_active, print_input_thread_started
    print_input_thread_active = True
    print_input_thread_started = True
    while print_input_thread_active == True:
        msg = readLine()
        if len(msg) > 0:
            print(msg)
    print_input_thread_started = False


def startPrintInputThread():
    print_thread = threading.Thread(target=printInputThread)
    print_thread.daemon = True
    print_thread.start()
    # time.sleep(2)



print_input_to_file_thread_active = False
print_input_to_file_thread_started = False
print_input_while_printing_to_file = True

output_file = 0

def printInputToFileThread():
    global print_input_to_file_thread_active,print_input_to_file_thread_started,print_input_while_printing_to_file
    print_input_to_file_thread_active = print_input_to_file_thread_started = True

    global arduino, output_file
    while print_input_to_file_thread_active == True:
        msg = readLine().strip()
        if len(msg) > 0:
            output_file.write(msg+"\r\n")
            if print_input_while_printing_to_file:
                print(msg)

    output_file.close()      
    print_input_to_file_thread_started = False

def startPrintInputToFileThread(filename):
    global output_file
    output_file = open(filename,"w")

    print_input_to_file_thread = threading.Thread(target=printInputToFileThread)
    print_input_to_file_thread.daemon = True
    print_input_to_file_thread.start()


    pass


def killThreads():

    global print_input_thread_active,print_input_thread_started
    global print_input_to_file_thread_active,print_input_to_file_thread_started

    print("KILLING THREADS")
    print_input_thread_active = False
    while print_input_thread_started == True:
        pass

    print_input_to_file_thread_active = False
    while print_input_to_file_thread_started == True:
        pass


    print("THREADS KILLED, READY TO FINISH")

def end():
    global arduino
    killThreads()
    arduino.close()

