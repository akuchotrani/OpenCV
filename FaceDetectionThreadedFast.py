# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:45:20 2018

@author: aakash.chotrani
"""
import cv2
from threading import Thread
import time
import face_recognition
from queue import Queue

def Timer(name,delay,repeat):
    print ("Timer:"+name+"Started")
    while repeat >0:
        time.sleep(delay)
        print (name+":"+str(time.ctime(time.time())))
        repeat -= 1
    print ("Timer:"+name+"completed")


# Load a sample picture and learn how to recognize it.
Aakash_image = face_recognition.load_image_file("Aakash_LinkedIn.jpg")
Aakash_face_encoding = face_recognition.face_encodings(Aakash_image)[0]

shivam_image = face_recognition.load_image_file("shivam.jpg")
shivam_face_encoding = face_recognition.face_encodings(shivam_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    Aakash_face_encoding,
    shivam_face_encoding
]
known_face_names = [
    "Aakash",
    "Shivam"
]


Shared_Data_Queue = Queue()

def StartWebCamAndRenderFrames():
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720);
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
    thread_started = False
    
    FPS = 0
    start_time = time.time()
    while True:
        FPS += 1
        if(time.time() > start_time + 1):
            print('FPS: ',FPS)
            FPS = 0
            start_time = time.time()
        ret,frame = video_capture.read()
        Shared_Data_Queue.put(frame)
        
        if (thread_started == False):
            thread_started = True
            
#        Recognition_Face(frame)
        # Display the resulting image
        cv2.imshow('Video', frame)
        
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def Recognition_Face():
    print("face recognition called\n")
    while True:
        print("Recognizing faces\n")
        currentFrame = Shared_Data_Queue.get()
        rgb_frame = currentFrame[:, :, ::-1]
    
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    #     Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    
            name = "Unknown"
    
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print("Recognized: ",name)
    
#            # Draw a box around the face
#            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#    
#            # Draw a label with a name below the face
#            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#            font = cv2.FONT_HERSHEY_DUPLEX
#            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            
            
            
            

        
    

def Main():
#    t1 = Thread(target = Timer,args = ("Timer1",1,5))
#    t2 = Thread(target = Timer, args = ("Timer 2",2,5))
#    t1.start()
#    t2.start()
    
    webcamThread = Thread(target = StartWebCamAndRenderFrames)
    webcamThread.setDaemon(True)
    webcamThread.start()
    
#    time.sleep(5)
    
    recognizeFaceThread = Thread(target = Recognition_Face)
    recognizeFaceThread.setDaemon(True)
    recognizeFaceThread.start()

#    StartWebCamAndRenderFrames()
    
    
if __name__ == "__main__":
    Main()
