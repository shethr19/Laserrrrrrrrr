import gphoto2 as gp
import subprocess


#this funtions uses terminal to auto detect attached camera
def detect_cam():
	p = subprocess.Popen(["gphoto2", "--auto-detect"], stdout=subprocess.PIPE)
	print p.communicate()[0] + "Connection Successful"

def set_iso():
	p = subprocess.Popen(["gphoto2", "--set-config-value iso = '100'"], stdout=subprocess.PIPE)
	print p.communicate()[0] + "ISO set"

def set_shutter_speed():
	p = subprocess.Popen(["gphoto2", "--get-config autofocus"], stdout=subprocess.PIPE)
	print p.communicate()[0] + ""

def Capture():
	p = subprocess.Popen(["gphoto2", "--capture-image-and-download"], stdout=subprocess.PIPE)
	print p.communicate()[0] + "TRIIGGGEERRRR"



detect_cam()
set_iso()
set_shutter_speed()
Capture()	