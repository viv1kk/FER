import face_recognition
import os
import numpy as np
import cv2

KNOWN_FACES_DIR = "./images/train/"
UNKNOWN_FACES_DIR = "./images/test/"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog" #hog


print("loading known Faces")

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = cv2.imread(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

known_names = np.array(known_names)
known_faces = np.array(known_faces)

# print(known_faces, known_names)


print("Processing Unknown faces")

for filename in os.listdir(UNKNOWN_FACES_DIR):
    print(filename)
    image = np.array(cv2.imread(f"{UNKNOWN_FACES_DIR}/{filename}"))
    locations = np.array(face_recognition.face_locations(image,  model = MODEL))
    encodings = face_recognition.face_encodings(image, locations)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # print(type(encoding))
    # print(encoding)
    # print(locations)
    # print(encoding)

    for face_encoding, face_location in zip(encodings, locations):
        results = np.array(face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE))
        # print(results)
        # print(type(results))

        match = "NONE"
        if True in results:
            match = known_names[np.where(results == True)]
            match = np.asarray(match)
            match = match[0]
            print(f"Match found: {match}")

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = [0, 255, 0]
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2])
            print(type(image), type(match))
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, str(match), (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(200,200,200), FONT_THICKNESS)
            
    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)