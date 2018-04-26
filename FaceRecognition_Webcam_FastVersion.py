# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 18:03:12 2018

@author: aakash.chotrani
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 17:14:14 2018

@author: aakash.chotrani
"""
import face_recognition
import cv2
import os
import time


known_face_names = [
#        'Aakash',
#        'Shivam'
]

# Create arrays of known face encodings and their names
known_face_encodings = [
#    Aakash_face_encoding,
#    shivam_face_encoding
]
 
def Get_Existing_Directories_Training_Images(path):
    
    for root, dirs, files in os.walk(path, topdown=False):    
        #for each directory that already exists get the name and push it to known faces array.
        for name in dirs:
            print(name)
            known_face_names.append(name)
            
            #Go in each directory and get the first image and call Train on the image.
            #NOTE BUG: Check if there are files in the directory.
            for rootx, dirsx, filesx in os.walk(os.path.join(root, name), topdown=False):
                print(filesx)
                print(os.path.join(root, name)+'/'+filesx[0])
                imagePath = os.path.join(root, name)+'/'+filesx[0]
                Train_Known_Person(imagePath)
                
                
#########################################################################################################
def Train_Known_Person(path):
    global known_face_encodings
    print('Training on known image:',path)
    known_person_face_image = face_recognition.load_image_file(path)
    known_person_face_encoding = face_recognition.face_encodings(known_person_face_image)[0]
    known_face_encodings.append(known_person_face_encoding)
                
#########################################################################################################
#########################################################################################################
    
    
    
Image_Capture_Delay_Seconds = 10

img_counter = 0
def capture_images(name,top,right,bottom,left):
    print('capture images called for name:',name)
    global img_counter
    #Resetting the path and names
    img_name = ""
    path = ""
    
    #saving the faces
    img_name = name+ str(img_counter) + '.jpg'
    crop_img = frame[top:bottom,left:right]
    
    #giving folder path to store the captured images.
    path = 'C:/Users/aakash.chotrani/Desktop/OpenCV/FaceRecognitionImages' +'/'+name
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(os.path.join(path,img_name),crop_img)
    img_counter = img_counter + 1
    print(img_counter," ",path+img_name)
    
    return path

#########################################################################################################
       
        
def Train_New_Person(name,face_locations):
    
    global known_face_encodings
    global known_face_names
    top = face_locations[0][0]
    right = face_locations[0][1]
    bottom = face_locations[0][2]
    left = face_locations[0][3]
    
    path = capture_images(name,top,right,bottom,left)
    known_face_names.append(name)
    #image counter is increased in the capture image function hence decresasing it and storing in temp
    temp = img_counter - 1
    ImageName  = name + str(temp)
    
    print('Training New Person from:',path,' ImageName:',ImageName,'\n')
    new_person_face_image_path = face_recognition.load_image_file(os.path.join(path,ImageName) + '.jpg')
    print('Create Face Encoding for: ',os.path.join(path,ImageName))
    new_person_face_encoding = face_recognition.face_encodings(new_person_face_image_path)[0]
    
    known_face_encodings.append(new_person_face_encoding)

#########################################################################################################


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
end_time = time.time() + Image_Capture_Delay_Seconds
unknown_person_counter = 0

def Start_Webcam():
    
    global process_this_frame
    global unknown_person_counter
    video_capture = cv2.VideoCapture(0)
    global frame
    global end_time
    captureAllPeopleFlag = False
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
    
        # Only process every other frame of video to save time
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance = 0.5)
            name = "unknown"
    
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                    
                face_names.append(name)
    
    
    
        # Display the results
        print('CurrentTime:',time.time(),' CaptureTime:',end_time)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if(time.time() > end_time):
                capture_images(name,top,right,bottom,left)
                captureAllPeopleFlag = True
            #####################################Displaying the Box##############################
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            ######################################################################################
        if captureAllPeopleFlag == True:
            end_time = time.time() + Image_Capture_Delay_Seconds
            captureAllPeopleFlag = False


        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
#########################################################################################################
#########################################################################################################


def main():
    path = 'C:/Users/aakash.chotrani/Desktop/OpenCV/FaceRecognitionImages'
    Get_Existing_Directories_Training_Images(path)
    Start_Webcam()
#########################################################################################################


if __name__ == "__main__":
    main()
#########################################################################################################





