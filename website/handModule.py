import math,time
import cv2 as cv
import numpy as np
class FingerDetector():
	skinColourLowerBound = np.array([0,48,80], np.uint8)
	skinColourUpperBound = np.array([20,255,255], np.uint8)
	kernel = np.ones((5,5), np.uint8)

	# Function to detect color of the skin and remove background
	def removeNoise(self,focus):
		hsv = cv.cvtColor(focus, cv.COLOR_BGR2HSV_FULL)
		mask = cv.inRange(hsv, self.skinColourLowerBound, self.skinColourUpperBound)
		mask = cv.dilate(mask, self.kernel, iterations = 3)
		mask = cv.GaussianBlur(mask, (5,5), 100)
		return mask

	#Function to return end point of detected finger
	def detectFinger(self,image):
		
		noise = self.removeNoise(image)
		_,threshold=cv.threshold(noise, 100, 255, cv.THRESH_BINARY)
		_,contours,_=cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		contour=max(contours, key = cv.contourArea)
		epsilon=0.001*cv.arcLength(contour, True)
		handPolygon=cv.approxPolyDP(contour, epsilon, True)
		handHull=cv.convexHull(handPolygon, returnPoints=False)
		defects=cv.convexityDefects(handPolygon, handHull)
		if defects is not None:
			for i in range(defects.shape[0]):
				fingertip = tuple(contour[contour[:,:,1].argmin()][0])
				return fingertip
