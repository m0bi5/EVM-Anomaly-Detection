# import the necessary packages
import argparse
import cv2
 
cam=cv2.VideoCapture(0)
while True:
	ret,image = cam.read()
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
	#thresh = cv2.inRange(image, (0,0,0), (255,150,150))
	# find contours in the thresholded image and initialize the
	# shape detector
	_,cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	#cnt = sorted(cnts, key=cv2.contourArea)
	for cnt in cnts:
		polygonArc = cv2.arcLength(cnt,True)
		polygonFound = cv2.approxPolyDP(cnt, 0.1 * polygonArc,True)
		cv2.drawContours(image, [polygonFound], -1, (0, 255, 0), 1) 
	cv2.imshow('sad',image)
	if (cv2.waitKey(1) & 0xFF == ord('q')):
		break