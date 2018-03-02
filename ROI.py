# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 17:03:42 2018

@author: aakash.chotrani
"""

import cv2
import numpy as np



img = cv2.imread('Aakash.jpg',cv2.IMREAD_COLOR)

#ROI: Region of an image
roi = img[100:150,100:150]
print(roi)

img[100:150,100:150] = [255,0,255]
 
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()