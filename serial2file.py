import serialduino


# serialduino.baud_rate = 115200
# serialduino.port = "COM3"


serialduino.baud_rate = 2000000
serialduino.connection_succes_msg = "{!!}\r\n"
serialduino.port = "COM7"
file_name = "serial_input.txt"

if not serialduino.connect() :
    print("BYE")
    exit()


serialduino.startPrintInputToFileThread(file_name)

print("START")


while True:
 
   
    print(">>>>")
    key = input()
   

    if(key == 'exit' or key == 'end') :       
        break
    else :
        serialduino.sendStr(key)
 
 
 
serialduino.end()
print("FINISH")