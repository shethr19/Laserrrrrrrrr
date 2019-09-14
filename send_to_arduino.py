from time import sleep
from tkinter import filedialog
from tkinter import *
import serial

# file-selector
# filename = '/home/ben/Desktop/laserHTN/textCoordinates.txt'
root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
# print ('file: ' + root.filename)

f = open(root.filename, 'r')

# serial setup
laserElectronics = serial.Serial(
	port = '/dev/cu.usbmodem14101',
	baudrate = 9600,
	timeout = 5
)

# transmit to Arduino
for line in f:
	laserElectronics.write(line.encode())
	sleep(2)
f.close()
