from django.shortcuts import render,redirect
from django.http import StreamingHttpResponse
import cv2,threading,main
from django.views.decorators.gzip import gzip_page
from django.template import loader, Context

import math,time,requests
import cv2 as cv 
import numpy as np
from buttonModule import ButtonDetector
from handModule import FingerDetector
from azureModule import TalkToAzure
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class VideoCamera(object):
    buttonFrames=0
    buttons=[]
    fingerDetectorObject=FingerDetector()
    transactionObject=TalkToAzure()
    transactionObject.transactionInit()
    voted=False
    transactionReceipt=None
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        if self.grabbed:
            if self.buttonFrames<100:
                buttonDetectorObject=ButtonDetector()
                #Start vote button detection cycle
                self.buttons=buttonDetectorObject.getBoundingBoxes(image)
                self.buttonFrames+=1
            for button in self.buttons:
                cv.drawContours( image, [button], -1, ( 255, 0, 0 ), 2 )
            finger=self.fingerDetectorObject.detectFinger(image) 
            cv.circle(image, finger, 5, [0,255,0], -1)  
            for i in range(len(self.buttons)):
                boxCoordinates=[self.buttons[i][j][0] for j in range(4)]
                fingerPoint=Point(finger[0],finger[1])
                voteButton=Polygon(boxCoordinates)
                if voteButton.contains(fingerPoint):
                    if i!=choiceCount['choice']:
                        choiceCount['frameCount']=0
                    choiceCount['choice']=i
                    choiceCount['frameCount']+=1
                    if choiceCount['frameCount']==20:
                        print('Voted for ',choiceCount['choice'])
                        self.voted=True
                        self.buttonFrames=0
                        #Send transaction to Azure Blockchain
                        self.transactionReceipt=self.transactionObject.makeTransaction(self.transactionObject.contract.functions.cast_vote(choiceCount['choice']))
                        
                        #return redirect('voted',self.transactionReceipt['transactionHash'].hex())

            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()



# Create your views here.
def home(request):
    return render(request,'home.html',{})

def voted(request,transactionHash):
    return render(request,'voted.html',{'transactionHash':transactionHash})
choiceCount={"choice":-1,"frameCount":0}




def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def video(request):
    cam = VideoCamera()
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass