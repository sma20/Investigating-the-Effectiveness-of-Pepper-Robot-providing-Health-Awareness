import numpy as np
import face_recognition
import os

faces_to_compare = []
names = []
for file in os.listdir("static/captures/"):
    if file.endswith(".jpg"):
        names.append(file)

# * ---------- Encode the nameless picture --------- *
# Load picture
face_picture = face_recognition.load_image_file("static/captures/"+names[0])
face_encoding_a1 = face_recognition.face_encodings(face_picture)[0]


for name in names:

    face_picture1 = face_recognition.load_image_file("static/captures/"+name)


    face_encoding_a2 = face_recognition.face_encodings(face_picture1)[0]

    faces_to_compare.append(face_encoding_a2)


matches = face_recognition.compare_faces(faces_to_compare, face_encoding_a2)


for match in matches:
    if match == True:
        print(match)
