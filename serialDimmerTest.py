import serialduino, time, random
 
def createRandomRGB():
    o = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    return o



# def setRGB(rgb):
#     str = "R{},{},{}"
#     serialduino.sendStr(str.format(rgb[0],rgb[1],rgb[2]))


def setRGB(r,g = 0,b = 0):
    str = "R{},{},{}"
    if(type(r) == tuple):
         serialduino.sendStr(str.format(r[0],r[1],r[2]))
    else:
        serialduino.sendStr(str.format(r,g,b))


def sendCommand(command):
    serialduino.sendStr("C"+str(command))

serialduino.baud_rate = 115200
serialduino.port = "COM5"

if not serialduino.connect() :
    print("BYE")
    exit()


serialduino.startPrintInputThread()
sendCommand(3)
print("START")

while True:
 
   
    print(">>>>")
    key = input()
   

    if(key == "r") :
       
        
        setRGB(createRandomRGB())
        time.sleep(0.5)

  

    elif(key == 'exit' or key == 'end') :       
        break
    else :
        serialduino.sendStr(key)
 

sendCommand(2)
serialduino.end()


print("FINISH")