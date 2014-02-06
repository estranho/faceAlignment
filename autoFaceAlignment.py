import os
import sys
import numpy as np
import cv2
import pyvision as pv
import pyvision.face.CascadeDetector as cd
import pyvision.face.FilterEyeLocator as ed
import pyvision.types.Affine
import Image

face_detect = cd.CascadeDetector("haarcascade_frontalface_alt.xml")
eye_detect = ed.FilterEyeLocator("EyeLocatorASEF128x128.fel")

destiny = sys.argv[2]
if not destiny.endswith("/"):
    destiny+="/"

for files in os.listdir(sys.argv[1]):
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".ppm"):
        temp = cv2.imread(sys.argv[1]+files,0)
        cols = temp.shape[0]
        rows = temp.shape[1]        
        im = np.ones((rows+200,cols+200),dtype = np.float32)
        im[100:rows+100,100:cols+100] = np.transpose(temp)/255.0        

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

        affine = pv.AffineFromPoints(left_eye, right_eye, pv.Point(62.5,115), pv.Point(137.5,115), (200,250))
        tile = affine(im)
        name = files[0:-3]+"png"
        tile.save(destiny+name)
