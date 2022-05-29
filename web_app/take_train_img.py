from cgitb import small
import time
import cv2
import dlib
import os
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner
import face_recognition

def create_dataset(roll):

	Num = 1
	face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	id=roll 
	vs = (VideoStream(src=0)).start()
	# Capturing the faces one by one and storing into folder
	while(True):
		print(Num)
		frame = vs.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_detector.detectMultiScale(gray, 1.3, 5)
		id = roll
		for (x,y,w,h) in faces:
			cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
			cv2.imwrite("Data/Roll." + str(roll) + '.' + str(Num) + ".jpg", gray[y:y+h,x:x+w])
        	# Display the video frame, with bounded rectangle on the person's face
		Num += 1
		cv2.imshow('Press ESC to quit', frame)
    # To stop taking video, press 'q' for at least 100ms
		if cv2.waitKey(100) & 0xFF == ord('q'):
			break

    # If image taken reach 100, stop taking video
		elif Num>50:
			break
		#Stoping the videostream
	vs.stop()
	# 	#destroying all the camera window
	cv2.destroyAllWindows()

