# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:27:53 2018

@author: aakash.chotrani
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)


while True:
    ret,frame = cap.read()
    cv2.imshow('frame',frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()