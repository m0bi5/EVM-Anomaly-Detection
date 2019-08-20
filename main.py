import math,time,requests
import cv2 as cv 
import numpy as np
from buttonModule import ButtonDetector
from handModule import FingerDetector
from azureModule import TalkToAzure
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
imageToButton={
    0:2,
    1:0,
    2:1
}
buttons=[]
buttonDetectorObject=ButtonDetector()
fingerDetectorObject=FingerDetector()
transactionObject=TalkToAzure()
transactionObject.transactionInit()
voted=False
transactionReceipt=None
camera = cv.VideoCapture(0)  

calibrationFrames=0
print("Detecting vote buttons, please wait")
#Start vote button detection cycle
while camera.isOpened():
    ret,image=camera.read()
    buttons=buttonDetectorObject.getBoundingBoxes(image)
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
    finger=fingerDetectorObject.detectFinger(image) 
    cv.circle(image, finger, 5, [0,255,0], -1)  
    for i in range(len(buttons)):
        boxCoordinates=[buttons[i][j][0] for j in range(4)]
        contourMoment = cv.moments(buttons[i])
        centerX = int(contourMoment["m10"] / contourMoment["m00"])
        centerY = int(contourMoment["m01"] / contourMoment["m00"])	
        cv.putText(image, str(i), (centerX, centerY),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv.putText(image, str(imageToButton[i]), (centerX, centerY-int(cv.arcLength(buttons[i],True)/4)),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        fingerPoint=Point(finger[0],finger[1])
        voteButton=Polygon(boxCoordinates)
        if voteButton.contains(fingerPoint):
            if i!=choiceCount['choice']:
                choiceCount['frameCount']=0
            choiceCount['choice']=i
            choiceCount['frameCount']+=1
            if choiceCount['frameCount']==20:
                print('Voted for ',choiceCount['choice'], ' according to image')
                print('Voted for ',imageToButton[choiceCount['choice']], ' according to button')
                if choiceCount['choice']!=imageToButton[choiceCount['choice']]:
                    print("EVM HACKED!!!")
                voted=True
                #Send transaction to Azure Blockchain
                transactionReceipt=transactionObject.makeTransaction(transactionObject.contract.functions.cast_vote(choiceCount['choice']))
                break

        cv.drawContours( image, [buttons[i]], -1, ( 255, 0, 0 ), 2 )
    cv.imshow('out',image)
    if (cv.waitKey(1) & 0xFF == ord('q')) or voted:
        break
cv.destroyAllWindows()
camera.release()
print(transactionReceipt)
'''
URL = 'http://localhost:8000'
dataToSend={'transactionHash':transactionReceipt['transactionHash'].hex(),'blockNumber':transactionReceipt['blockNumber']}
print(dataToSend)
requests.post(URL,data=dataToSend,headers=dict(Referer=URL))'''