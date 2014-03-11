import os
import sys
import csv
import numpy as np
import cv2
import pyvision as pv
import pyvision.types.Affine
import Image

ifile = open(sys.argv[1],"rb")
reader = csv.reader(ifile)

for row in reader:
    path = sys.argv[1].replace(sys.argv[1].split('/')[-1],'')
    try:
        img = pv.Image(path+row[0])
    except:
        continue
    #cols = temp.shape[0]
    #rows = temp.shape[1]        
    #im = np.ones((rows+200,cols+200),dtype = np.float32)
    #im[100:rows+100,100:cols+100] = np.transpose(temp)/255.0        

    #im = pv.Image(im)
    #im = pv.Image(im.asPIL())
    
    left_eye = pv.Point(float(row[1]),float(row[2]))
    right_eye = pv.Point(float(row[3]),float(row[4]))
    center_of_eyes = pv.Point((float(row[1])+float(row[3]))/2,(float(row[2])+float(row[4]))/2)
    mouth = pv.Point(float(row[5]),float(row[6]))

    affine = pv.AffineFromPoints(center_of_eyes, mouth, pv.Point(100,110), pv.Point(100,188), (200,250))

    tile = affine(img)
    name = row[0]
    tile.save(path+name)
