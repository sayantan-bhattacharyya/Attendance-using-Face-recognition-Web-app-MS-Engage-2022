import cv2
import os
import numpy as np
from PIL import Image
import imutils
from imutils.video import VideoStream


def attendance_taker():

    Roll_present=[]
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the trained mode
    recognizer.read('trainer/trainer.yml')

    # Load prebuilt model for Frontal Face
    cascadePath = "haarcascade_frontalface_default.xml"

    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);

    # Set the font style
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start the video frame capture
    cam = (VideoStream(src=0)).start()

    # Loop
    while True:
        # Read the video frame
        im =cam.read()

        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.3,5)

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

            # Recognize the face belongs to which ID
            Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check the ID if exist 
            if(100 - confidence)>50:
                if int(Id) in Roll_present:
                    pass
                else:
                    Roll_present.append(int(Id))
            else:
                Id = "Unknown" 

            # Put text describe who is in the picture
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 1, (255,255,255), 3)
        cv2.imshow('Cam----Press q to quit',im)

    # Display the video frame with the bounded rectangle
             

    # If 'q' is pressed, close program
        if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Stop the camera
    cam.stop()

    # Close all windows
    cv2.destroyAllWindows()

    return Roll_present