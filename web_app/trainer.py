import cv2
import os
import numpy as np
from PIL import Image

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    dataPath = os.path.join('Data/')

    images = []
    labels=[]

    images, labels = getImagesAndLabels(dataPath)
    recognizer.train(images, np.array(labels))
    recognizer.save(os.path.join('trainer/trainer.yml'))
    cv2.destroyAllWindows()

def getImagesAndLabels(Path):

    # Get all file path
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imagePaths = [os.path.join(Path,f) for f in os.listdir(Path)] 
    
    # Initialize empty face sample
    faceSamples=[]
    
    # Initialize empty id
    ids = []

    # Loop all the file path
    for imagePath in imagePaths:

        # Get the image and convert it to grayscale
        PIL_img = Image.open(imagePath).convert('L')

        # PIL image to numpy array
        img_numpy = np.array(PIL_img,'uint8')

        # Get the image id
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # Get the face from the training images
        faces = detector.detectMultiScale(img_numpy)

        # Loop for each face, append to their respective ID
        for (x,y,w,h) in faces:

            # Add the image to face samples
            faceSamples.append(img_numpy[y:y+h,x:x+w])

            # Add the Roll no.s to IDs
            ids.append(id)
            cv2.imshow("Adding faces to traning set...", img_numpy[y: y + h, x: x + w])
            cv2.waitKey(5)

    # Pass the face array and IDs array
    return faceSamples,ids
