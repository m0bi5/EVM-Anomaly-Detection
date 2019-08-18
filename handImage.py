## @Author: Dishant Varshney
""" Finger Tracking: This pyhton program tracks the finger """
import numpy as np 
import cv2 as cv 
import math

class fingerDetector():
	lwr = np.array([0,50,70], np.uint8)
	upr = np.array([100,230,230], np.uint8)
	kernel = np.ones((5,5), np.uint8)

	# Function to detect color of the skin
	def removeNoise(self,focus):
		hsv = cv.cvtColor(focus, cv.COLOR_BGR2HSV_FULL)
		mask = cv.inRange(hsv, self.lwr, self.upr)
		mask = cv.dilate(mask, self.kernel, iterations = 3)
		mask = cv.GaussianBlur(mask, (5,5), 100)
		return mask

	#Function to return end point of detected finger
	def detectFinger(self,image):
		noise = self.removeNoise(image)
		_,threshold=cv.threshold(noise, 100, 255, cv.THRESH_BINARY)
		_, contours,_=cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		contour=max(contours, key = cv.contourArea)
		epsilon=0.001*cv.arcLength(contour, True)
		handPolygon=cv.approxPolyDP(contour, epsilon, True)
		handHull=cv.convexHull(handPolygon, returnPoints=False)
		defects=cv.convexityDefects(handPolygon, handHull)
		if defects is not None:
			for i in range(defects.shape[0]):
				ftop = tuple(contour[contour[:,:,1].argmax()][0])
				return ftop