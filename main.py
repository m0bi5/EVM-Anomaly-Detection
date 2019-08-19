import math,time
import cv2 as cv 
import numpy as np
from buttonModule import buttonDetector
from handModule import fingerDetector
from azureModule import talkToAzure
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

buttons=[]
buttonDetectorObj=buttonDetector()
fingerDetectorObj=fingerDetector()
voted=False
camera = cv.VideoCapture(0)  

calibrationFrames=0
print("Detecting vote buttons, please wait")
#Start vote button detection cycle
while camera.isOpened():
    ret,image=camera.read()
    buttons=buttonDetectorObj.getBoundingBoxes(image)
    for button in buttons:
        cv.drawContours( image, [button], -1, ( 255, 0, 0 ), 2 )
    cv.imshow('Button Detection',image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    calibrationFrames+=1
    if calibrationFrames==100:
        break
print('Vote buttons detected')
cv.destroyAllWindows()
choiceCount={"choice":-1,"frameCount":0}

#Start finger tracking cycle
while camera.isOpened():
    ret,image=camera.read() 
    finger=fingerDetectorObj.detectFinger(image) 
    print(choiceCount)
    cv.circle(image, finger, 5, [0,255,0], -1)  
    for i in range(len(buttons)):
        boxCoordinates=[buttons[i][j][0] for j in range(4)]
        fingerPoint = Point(finger[0],finger[1])
        voteButton = Polygon(boxCoordinates)
        if voteButton.contains(fingerPoint):
            if i!=choiceCount['choice']:
                choiceCount['frameCount']=0
            choiceCount['choice']=i
            choiceCount['frameCount']+=1
            if choiceCount['frameCount']==20:
                print('Voted for ',choiceCount['choice'],i)
                voted=True
                break

        cv.drawContours( image, [buttons[i]], -1, ( 255, 0, 0 ), 2 )
    cv.imshow('out',image)
    if (cv.waitKey(1) & 0xFF == ord('q')) or voted:
        break
cv.destroyAllWindows()

camera.release()