# import the necessary packages
import argparse
import cv2
 
image = cv2.imread('rect_evm.jpg')

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.inRange(image, (100,0,0), (255,110,100))

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_NONE)[1]
cnt = sorted(cnts, key=cv2.contourArea)
cv2.drawContours(image, cnts, -1, (0, 255, 0), 1) 
cv2.imshow("buttons", image)
cv2.waitKey(0)