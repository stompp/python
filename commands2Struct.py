inputFile = open('commands.txt','r')
lines = inputFile.readlines()

outputFile = open('commands_output.txt','w')
struct_name = "RGBDimmerCommand"
def writeLine(str, indent = 0):
    global outputFile
    for n in range(indent):
        outputFile.write("\t")
    outputFile.write(str + "\n")


writeLine("struct {}".format(struct_name)+"{")


n = 0
for line in lines:
    if len(line.strip()):
        writeLine("static const uint8_t {} = {};".format(line.strip(), n),1)
        # outputFile.write("{} = {};\n".format(line.strip(), n))
        n +=1
    else: 
        outputFile.write("\n")

writeLine("};")

outputFile.write("\n")


#commands swith
writeLine("switch(command){")

for line in lines:
    if(len(line.strip())):
        writeLine("case {}::{}:".format(struct_name,line.strip()),1)
        writeLine("",2)
        writeLine("break;",2)    

writeLine("default:",1)
writeLine("break;",2)

writeLine("\n}")
# for line in lines:
# # writing to file
# file1 = open('myfile.txt', 'w')
# file1.writelines(L)
# file1.close()
 
# # Using readlines()
# file1 = open('myfile.txt', 'r')
# Lines = file1.readlines()
 
# count = 0
# # Strips the newline character
# for line in Lines:
#     count += 1
#     print("Line{}: {}".format(count, line.strip()))