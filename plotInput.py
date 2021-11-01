import serialduino,plotFile,time


serialduino.baud_rate = 115200
serialduino.connection_succes_msg = "{!!}\r\n"
serialduino.port = "COM3"
plotFile.file_name = "serial_input.txt"

time_out = 2
if not serialduino.connect() :
    print("BYE")
    exit()


serialduino.startPrintInputToFileThread(plotFile.file_name)

print("START")

while time_out > 0:
    print(time_out)
    time.sleep(1)
    time_out -= 1
 
serialduino.end()
print("FINISH")
plotFile.plot()


