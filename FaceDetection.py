# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:17:02 2018

@author: aakash.chotrani
"""

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('Aakash_snow_video.MOV')

img_name_counter = 1
extension = ".png"
while True:
    ret,img = cap.read()
    if ret == True:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for(ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            img_name_counter +=1;
            img_name = str(img_name_counter) + extension
            crop_img = img[y:y+h, x:x+w]
            cv2.imwrite(img_name,crop_img)
            cv2.imshow("cropped", crop_img)

            
        cv2.imshow('img',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Video stream ended")
        break


cap.release()
cv2.destroyAllWindows()


#img = cv2.imread('Aakash.jpg',cv2.IMREAD_COLOR)
#while True:
#    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#    faces = face_cascade.detectMultiScale(gray,1.3,5)
#    for (x,y,w,h) in faces:
#        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#        roi_gray = gray[y:y+h, x:x+w]
#        roi_color = img[y:y+h, x:x+w]
#        eyes = eye_cascade.detectMultiScale(roi_gray)
#        for(ex,ey,ew,eh) in eyes:
#            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#        cv2.imshow('img',img)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#        break
#    break


