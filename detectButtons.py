import cv2
import time
import numpy as np

class buttonDetector():
    image=None

    boxToParty={
        0:"Party A",
        1:"Party B",
        2:"Party C"
    }

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
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 1, 10, 120)
        edges  = cv2.Canny(gray, 10,250)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
        closed = cv2.morphologyEx( edges,cv2.MORPH_CLOSE,kernel)
        _,contours,_ = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
        for contour in contours:
            if cv2.contourArea(contour) > 5000 :
                polygonArc = cv2.arcLength(contour,True)
                polygonFound = cv2.approxPolyDP(contour, 0.1 * polygonArc,True)
                if (len(polygonFound)==4):
                    boxes.append(polygonFound)
        return boxes
