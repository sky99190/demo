import serial
import time
import binascii
from imutils.video.pivideostream import PiVideoStream
import numpy as np
import copy
import smbus
import time

import cv2,time

vs = PiVideoStream()

vs.camera.vflip=True
vs.camera.brightness=50
vs.camera.iso=800
def get_distance():
	bus.write_byte_data(0x29,0x00,0x01)
	while True:
		state=bus.read_byte_data(0x29,0x14)
		if (state)&0x01:
			break
	#print(state&0x78)
	data=bus.read_byte_data(0x29,0x1e)
	data2=bus.read_byte_data(0x29,0x1f)
	data3=(data<<8)|data2
	#time.sleep(0.05)
	return [data3,state]

bus=smbus.SMBus(1)
ser=serial.Serial('/dev/ttyUSB0',115200,timeout=1)

ser.flushInput()

while True:
	count=ser.inWaiting()
	if count!=0:
		rect=ser.read(count)
		print(rect)
		if rect=='on':
			print('system start')
			break
	ser.flushInput	
	#ser.write('a')
	#ser.flushInput()
	time.sleep(0.5)

kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#fgbg=cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg=cv2.createBackgroundSubtractorKNN()
fgbg=cv2.createBackgroundSubtractorMOG2(history=150,varThreshold=200,detectShadows=False)


kernel2=np.ones((3,3),np.uint8)

vs.start()
time.sleep(2)
image=vs.read()
ofgbg=copy.deepcopy(fgbg)
fgmask=fgbg.apply(image)
fgmask=cv2.morphologyEx(fgmask,cv2.MORPH_OPEN,kernel2)

counter=0
counter2=0
while(True):
	#counter+=1
	fgmask=fgbg.apply(image)
	#fgmask=cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
	#dst=cv2.GaussianBlur(image,(5,5),0)
	[distance , state]= get_distance()
	if (state&0x78)==64 or (state&0x78)==72:
		print("outofrange")
	else:
		print(distance)
	cv2.imshow("origin",image)
	cv2.imshow("fgmask",fgmask)
	image=vs.read()
	if np.count_nonzero(fgmask)>1000:
		counter+=1
		counter2=0
	else:
		counter2+=1
	print(np.count_nonzero(fgmask))
	if counter>=5:
		print('Movement Detect!!!')
	if counter2>=10:
		counter=0
	count=ser.inWaiting()
	if count!=0:
		rect=ser.read(count)
		print(rect)
		if rect=='off':
			print('system end')
			ser.flushInput	
			break
	
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()
time.sleep(0.5)
