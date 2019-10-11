import cv2,time
from imutils.video.pivideostream import PiVideoStream
import numpy as np
import copy
vs = PiVideoStream()

vs.camera.vflip=True
vs.camera.brightness=50
vs.camera.iso=800

kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg=cv2.createBackgroundSubtractorMOG2(history=150,varThreshold=200,detectShadows=False)
kernel2=np.ones((3,3),np.uint8)

vs.start()
time.sleep(2)
image=vs.read()
ofgbg=copy.deepcopy(fgbg)
fgmask=fgbg.apply(image)
fgmask=cv2.morphologyEx(fgmask,cv2.MORPH_OPEN,kernel2)

counter=0
while(True):
	counter+=1
	fgmask=fgbg.apply(image)
	cv2.imshow("origin",image)
	cv2.imshow("fgmask",fgmask)
	image=vs.read()
	print(np.count_nonzero(fgmask))

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
vs.stop()
time.sleep(0.5)
