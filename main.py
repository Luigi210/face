import cv2
import random as rd
import os
from deepface import DeepFace
# import dlib
# import face_recognition
# import cmake
# import dlib

# cv2.Vide
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

img_path = r'C:\\Users\\akhme\\Desktop\\diploma\\images'
os.chdir(img_path)

def takePhoto(path: str, img: any):
    if isUnique(path):
        cv2.imwrite(path, img)
        cv2.destroyAllWindows()

def isUnique(img):
    unique = True
    for file in os.listdir(img_path):
        if img == file:
            unique = False
    return unique

while True:
    success, img = cap.read()
    cv2.imshow("Face Attendace", img)
    if cv2.waitKey(1) & 0xFF == ord('y'):
        # print(os.listdir(img_path))
        takePhoto('image' + str(rd.randint(1, 1500000)) + '.png', img)
        break

cap.release()
