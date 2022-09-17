import face_recognition
import os
import cv2
import numpy as np

KNOWN_FACES_DIR = "./images/train/"
UNKNOWN_FACES_DIR = "./images/test/"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog" #hog, cnn

print("loading known Faces")

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")

        # encoding will return the numpy arrays of all the faces found in the image 
        encoding = face_recognition.face_encodings(image)
        print(np.shape(encoding))
        known_faces.append(encoding)
        known_names.append(name)



