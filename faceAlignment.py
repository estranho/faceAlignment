import pyvision as pv
import pyvision.face.CascadeDetector as cd
import pyvision.face.FilterEyeLocator as ed
import pyvision.types.Affine
import math
import os
import sys

face_detect = cd.CascadeDetector("haarcascade_frontalface_alt.xml")
eye_detect = ed.FilterEyeLocator("EyeLocatorASEF128x128.fel")

destiny = sys.argv[2]
if not destiny.endswith("/"):
    destiny+="/"
i=0

for files in os.listdir(sys.argv[1]):
    if(i>=11000):
        break
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".ppm"):
        im = pv.Image(sys.argv[1]+files)
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

        affine = pv.AffineFromPoints(left_eye, right_eye, pv.Point(150,250), pv.Point(250,250), (400,500))
        tile = affine(im)
        name = files[0:-3]+"png"
        tile.save(destiny+name)

        i+=1
