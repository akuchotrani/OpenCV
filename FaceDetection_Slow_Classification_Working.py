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

def Train_Known_Person(path):
    global known_face_encodings
    
    known_person_face_image = face_recognition.load_image_file(path)
    known_person_face_encoding = face_recognition.face_encodings(known_person_face_image)[0]
    
    #record the encoding
    known_face_encodings.append(known_person_face_encoding)
                

Image_Capture_Delay_Seconds = 10

img_counter = 0
def capture_images(name,top,right,bottom,left):
    print('capture images called')
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

       
        
def Train_New_Person(name,face_locations):
    global known_face_encodings
    global known_face_names
    top = face_locations[0][0]
    right = face_locations[0][1]
    bottom = face_locations[0][2]
    left = face_locations[0][3]
    
#    top *= 4
#    right *= 4
#    bottom *= 4
#    left *= 4
    
    path = capture_images(name,top,right,bottom,left)
    
    #image counter is increased in the capture image function hence decresasing it and storing in temp
    temp = img_counter - 1
    name += str(temp)
    new_person_face_image = face_recognition.load_image_file(os.path.join(path,name) + '.jpg')
    new_person_face_encoding = face_recognition.face_encodings(new_person_face_image)[0]
    
    known_face_encodings.append(new_person_face_encoding)
    known_face_names.append(name)
    
    

# Load a sample picture and learn how to recognize it.
#Aakash_image = face_recognition.load_image_file("Aakash_LinkedIn.jpg")
#Aakash_face_encoding = face_recognition.face_encodings(Aakash_image)[0]

shivam_image = face_recognition.load_image_file("shivam.jpg")
shivam_face_encoding = face_recognition.face_encodings(shivam_image)[0]



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
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920);
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080);
    global frame
    global end_time
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

    
        # Resize frame of video to 1/4 size for faster face recognition processing
        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_frame = frame[:, :, ::-1]
    
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                
    
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                else:
                    name = "Person"+str(unknown_person_counter)
                    Train_New_Person(name,face_locations)
    #                Person_image = face_recognition.load_image_file("Aakash_LinkedIn.jpg")
    #                Aakash_face_encoding = face_recognition.face_encodings(Aakash_image)[0]
                    unknown_person_counter = unknown_person_counter + 1
                    
    
                face_names.append(name)
    
        process_this_frame = not process_this_frame
    
    
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#            top *= 4
#            right *= 4
#            bottom *= 4
#            left *= 4
            
            #capture image every few seconds
            if(time.time() > end_time):
                capture_images(name,top,right,bottom,left)
                end_time = time.time() + Image_Capture_Delay_Seconds
    
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
    
        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def main():
    path = 'C:/Users/aakash.chotrani/Desktop/OpenCV/FaceRecognitionImages'
    Get_Existing_Directories_Training_Images(path)
    Start_Webcam()


if __name__ == "__main__":
    main()







