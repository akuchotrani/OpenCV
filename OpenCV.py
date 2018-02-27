# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:10:00 2018

@author: aakash.chotrani
"""
#pip install opencv-python
import cv2
import numpy as np
import matplotlib.pyplot as plt



img = cv2.imread('Aakash.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#plt.imshow(img,cmap='gray',interpolation = 'bicubic')
#plt.plot([200,200],[400,1000],'c',linewidth = 5)
#plt.show()

cv2.imwrite('AakashGray.png',img)