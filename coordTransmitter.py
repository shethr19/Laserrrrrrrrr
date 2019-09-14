from tkinter import filedialog
from tkinter import *
import serial

# file-selector
filename = '/home/ben/Desktop/laserHTN/textCoordinates.txt'
# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/home/ben/Desktop",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
# print ('file: ' + root.filename)

f = open(root.filename, 'r')

# serial setup
laserElectronics = serial.Serial()
laserElectronics.baudrate = 9600
laserElectronics.port = 'COM5'
laserElectronics.timeout = 1


# transmit to Arduino
for line in f:
	print()

f.close()