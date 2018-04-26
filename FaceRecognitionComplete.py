# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 17:14:38 2018

@author: aakash.chotrani
"""

import face_recognition
import cv2
import os
from PIL import Image

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

#folders = []
#files = []
known_face_names = []
known_face_encodings = []

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/faces"

for entry in os.scandir(dir_path):
    if entry.is_dir():
        for entry2 in os.scandir(entry.path):
            if entry2.is_file():
                image = face_recognition.load_image_file(entry2.path)
                face_encodings = face_recognition.face_encodings(image)
                if len(face_encodings) == 0:
                    continue
                
                face_encoding = face_encodings[0]
                known_face_names.append(entry.name)
                known_face_encodings.append(face_encoding)
        
        
#for folder in folders:
#    for entry in os.scandir(folder):
#        if entry.is_file():
#            image = face_recognition.load_image_file(entry.path)
#            face_encoding = face_recognition.face_encodings(image)[0]
#            known_face_encodings.append(face_encoding)

video_capture = cv2.VideoCapture(0)
#video_capture = cv2.VideoCapture('Aakash_snow_video.MOV')   

#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
     
while True:

    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Unknown"
        
        lowest_distance = 1.0
        lowest_index = 0
        found = False
        
        for i, face_distance in enumerate(distances):
            
            if lowest_distance > face_distance:
                lowest_distance = face_distance
                lowest_index = i
            
#            if face_distance < 0.3:
#                first_match_index = matches.index(True)
#                name = known_face_names[first_match_index]
#                found = True
#                break
            
        if lowest_distance < 0.4:
                name = known_face_names[lowest_index]
                found = True

        if found == False:
            face_image = frame[top:bottom, left:right]    
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            
            if (fm < 200) :
                continue
            
            if lowest_distance < 0.6:
                name = known_face_names[lowest_index]
                dir_name = dir_path + "/" + name
                cv2.imwrite(dir_name + "/" + str(len(known_face_names)) + ".jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
            else:
                name = "face_" + str(len(known_face_names))
                dir_name = dir_path + "/" + name
                print('making a new directory:',dir_name)
                os.makedirs(dir_name)
                cv2.imwrite(dir_name + "/1.jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)


#        if True in matches:
#            first_match_index = matches.index(True)
#            name = known_face_names[first_match_index]
#        else:
#            face_image = frame[top:bottom, left:right]     
#            
#            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
#            fm = variance_of_laplacian(gray)
#            
#            print(fm)
#            
#            if (fm < 200) :
#                continue
#            
#            name = "face_" + str(len(known_face_names))
#            dir_name = dir_path + "/" + name
#            os.makedirs(dir_name)
#            cv2.imwrite(dir_name + "/face.jpg", face_image)
#            known_face_names.append(name)
#            known_face_encodings.append(face_encoding)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()