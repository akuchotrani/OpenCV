# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:27:53 2018

@author: aakash.chotrani
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

#Using system webcam
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('Aakash_snow_video.MOV')


while (cap.isOpened()):
    ret,frame = cap.read()
    
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Video stream ended")
        break
    
cap.release()
cv2.destroyAllWindows()