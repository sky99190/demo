import smbus
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation


xarr = []
yarr = []
count = 0
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global count
    [distance , state]= get_distance()
    if (state&0x78)==64 or (state&0x78)==72:
		pass
    else:
		count = count + 1
		xarr.append(count)
		yarr.append(distance)
		ax1.clear()
		ax1.plot(xarr,yarr)

bus=smbus.SMBus(1)

def get_distance():
	bus.write_byte_data(0x29,0x00,0x01)
	while True:
		state=bus.read_byte_data(0x29,0x14)
		if (state)&0x01:
			break
	data=bus.read_byte_data(0x29,0x1e)
	data2=bus.read_byte_data(0x29,0x1f)
	data3=(data<<8)|data2
	return [data3,state]
	
	
while True:
	t1=time.time()
	[distance , state]= get_distance()
	if (state&0x78)==64 or (state&0x78)==72:
		print("outofrange")
	else:
		print(distance)
		t2=time.time()


		

#ani = animation.FuncAnimation(fig, animate, interval=10)
#plt.show()
