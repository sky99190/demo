import serial
import time
ser=serial.Serial('/dev/ttyUSB0',115200,timeout=1)

ser.flushInput()

while True:
	count=ser.inWaiting()
	if count!=0:
		rect=ser.read(count)
		print(rect)
	ser.flushInput	
	#ser.write('a')
	#ser.flushInput()
	time.sleep(0.5)

ser.close()

