from detectButtons import buttonDetector
from handImage import fingerDetector
import cv2 as cv 
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

boxes=[]
buttonDetectorObj=buttonDetector()
fingerDetectorObj=fingerDetector()
camera = cv.VideoCapture(0)  

calibrationFrames=0
print("Detecting vote buttons, please wait")
#Start vote button detection cycle
while camera.isOpened():
    ret,image=camera.read()
    boxes=buttonDetectorObj.getBoundingBoxes(image)
    for box in boxes:
        cv.drawContours( image, [box], -1, ( 255, 0, 0 ), 2 )
    cv.imshow('box detection',image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    calibrationFrames+=1
    if calibrationFrames==100:
        break
print('Vote buttons detected')
cv.destroyAllWindows()

#Start finger tracking cycle
while camera.isOpened():
    ret,image=camera.read() 
    finger=fingerDetectorObj.detectFinger(image) 
    cv.circle(image, finger, 5, [0,255,0], -1)  
    for i in range(len(boxes)):
        boxCoordinates=[boxes[i][j][0] for j in range(4)]
        fingerPoint = Point(finger[0],finger[1])
        voteButton = Polygon(boxCoordinates)
        if voteButton.contains(fingerPoint):
            print('Hand found in box ',i)
        cv.drawContours( image, [boxes[i]], -1, ( 255, 0, 0 ), 2 )
    cv.imshow('out',image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()

camera.release()