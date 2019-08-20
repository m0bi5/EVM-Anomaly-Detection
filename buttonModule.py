import math,time
import cv2 as cv 
import numpy as np
class ButtonDetector():

    corners = np.array(
        [
            [[0, 0]],
            [[0, 420]],
            [[600, 420]],
            [[600 , 0]],
        ],
        np.float32
    )

    #Function to get vote button regions
    def getBoundingBoxes(self,image):
        boxes=[]
        gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray, 1, 10, 120)
        edges  = cv.Canny(gray, 10,250)
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(7,7))
        closed = cv.morphologyEx( edges,cv.MORPH_CLOSE,kernel)
        _,contours,_ = cv.findContours( closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE )
        for contour in contours:
            if cv.contourArea(contour) > 50 :
                polygonArc = cv.arcLength(contour,True)
                polygonFound = cv.approxPolyDP(contour, 0.1 * polygonArc,True)
                #if (len(polygonFound)==4):
                boxes.append(polygonFound)
        return boxes
