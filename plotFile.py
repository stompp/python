import matplotlib.pyplot as plt
import os
file_name = "serial_input.txt"
delimiter = ','

def plotFile(file_name,delimiter):

    inputFile = open(file_name,'r')
    lines = inputFile.readlines()

    x = list()
    y = list()

    n = 0
    for line in lines:
        l = line.strip()
        values = l.split(delimiter)
        if(len(l)>0):
            if(len(values) == 2):
                x.append(float(values[0]))
                y.append(float(values[1]))
            elif(len(values) == 1):
                x.append(n)
                y.append(float(values[0]))
            n+=1

    # plotting the data
    plt.plot(x, y)
    # Adding the title
    plt.title(file_name + " Plot")
    # Adding the labels
    plt.ylabel("y-axis")
    plt.xlabel("x-axis")
    plt.show()

def plot():
    global file_name,delimiter
    plotFile(file_name,delimiter)





if __name__ == "__main__":
    plotFile(file_name,delimiter)
