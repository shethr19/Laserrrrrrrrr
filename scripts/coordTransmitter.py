from time import sleep
from tkinter import filedialog
from tkinter import *
import serial

# file-selector
filename = '/home/ben/Desktop/laserHTN/textCoordinates.txt'
# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/home/ben/Desktop",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
# print ('file: ' + root.filename)

f = open(filename, 'r')

# serial setup
laserElectronics = serial.Serial(
	port = '/dev/ttyACM0',
	baudrate = 9600,
	timeout = 1
)

# transmit to Arduino
for line in f:
	laserElectronics.transmit(line)
	sleep(2)
f.close()