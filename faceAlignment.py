import numpy as np
import cv2
import cv
import pyvision as pv
import pyvision.face.CascadeDetector as cd
import pyvision.face.FilterEyeLocator as ed
import pyvision.types.Affine
import Image
import math
import os
import sys

left_eye = pv.Point(0,0)
right_eye = pv.Point(0,0)

def click_on_eyes(event,x,y,flags,param):
    if event == cv2.EVENT_RBUTTONDOWN:
        global left_eye 
        left_eye = pv.Point(y,x)
        print left_eye
    if event == cv2.EVENT_LBUTTONDOWN:
        global right_eye
        right_eye = pv.Point(y,x)
        print right_eye

face_detect = cd.CascadeDetector("haarcascade_frontalface_alt.xml")
eye_detect = ed.FilterEyeLocator("EyeLocatorASEF128x128.fel")

manual=False
if len(sys.argv) == 4:
    if sys.argv[3] == '--manual':
        manual=True

destiny = sys.argv[2]
if not destiny.endswith("/"):
    destiny+="/"
i=0

for files in os.listdir(sys.argv[1]):
#    if(i>=11000):
#        break
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".ppm"):
        temp = cv2.imread(sys.argv[1]+files,0)
        cols = temp.shape[0]
        rows = temp.shape[1]        
        im = np.ones((rows+200,cols+200),dtype = np.float32)
        im[100:rows+100,100:cols+100] = np.transpose(temp)/255.0        

        if not manual:
            im = pv.Image(im)
            im = pv.Image(im.asPIL())
            faces = face_detect(im)
            eyes = eye_detect(im,faces)

            if len(eyes) == 0:
                print files + " no detect"
                continue 
            elif len(eyes[0])<3:
                print files
                continue       

            left_eye = eyes[0][1]
            right_eye = eyes[0][2]

        else:
            im = np.transpose(im)
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',click_on_eyes)

            while(1):
                cv2.imshow('image',im)
                k = cv2.waitKey(1) & 0xFF
                if k == 32:
                   im = pv.Image(im)
                   im = pv.Image(im.asPIL())
                   break
        
        affine = pv.AffineFromPoints(left_eye, right_eye, pv.Point(125,220), pv.Point(275,220), (400,500))
        tile = affine(im)
        name = files[0:-3]+"png"
        tile.save(destiny+name)
        print destiny+name

#        i+=1

cv2.destroyAllWindows()
