import cv2
import random as rd
import os
from deepface import DeepFace
import numpy as np
import time
# import dlib
import face_recognition as fc
from mtcnn import MTCNN
# import cmake
# import dlib

# cv2.Vide
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1120)


img_path = r'C:\\Users\\akhme\\Desktop\\diploma\\images'
os.chdir(img_path)

def takePhoto(path: str, img: any):
    if isUnique(path):
        cv2.imwrite(path, img)
        cv2.destroyAllWindows()

def deletePhoto(path):
    os.remove(img_path + '\\' + path)

def isUnique(img):
    unique = True
    for file in os.listdir(img_path):
        if img == file:
            unique = False
    return unique

def showEllipse(img, show=True):
    if show:
        ellipsedImg = cv2.ellipse(img, (640, 360), (300, 200), 90, 0, 360, (0, 255, 0), 5)
        # green_image = cv2.cvtColor(image, cv2.C)
        withText = cv2.putText(
            ellipsedImg, 
            'Лицо должно быть в области эллипса', 
            (50, 680), 
            cv2.FONT_HERSHEY_COMPLEX, 0.6, 
            (0, 255, 0), 1, 
            cv2.LINE_AA
        )
        cv2.imshow("Face Attendace", withText)
    else:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            img1 = DeepFace.extract_faces(img)
            x = img1[0]['facial_area']['x']
            w = img1[0]['facial_area']['w']
            y = img1[0]['facial_area']['y']
            h = img1[0]['facial_area']['h']
            normalized = img1[0]['face']
            randId = rd.randint(1, 1500000)
            takePhoto('image' + str(randId) + '.png', img)
            print(os.path.exists('image' + str(randId) + '.png'))
            time.sleep(3)
            takenPhoto = cv2.imread('image' + str(randId) + '.png')
            # takenPhoto = cv2.imread('')
            # deletePhoto('image' + str(randId) + '.png')
            # res = DeepFace.find()
            cropped = takenPhoto[x: x + w][y: y + h]
            dfs = DeepFace.find(cropped, db_path='C:/Users/akhme/Desktop/diploma/images')
            print(cropped, dfs)
            cv2.destroyAllWindows()

        cv2.imshow("Face Attendace", img)

def isOnePerson(img: any) -> bool:
    detector = MTCNN()
    detections = detector.detect_faces(img)
    print("Length", len(detections))
    return len(detections) == 1

while True:
    success, img = cap.read()
    face_blurred = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # face_located = fc.face_locations(face_blurred, model='cnn')
    if cv2.waitKey(1) & 0xFF == ord('o'):
        print("clicked")
        if not isOnePerson(face_blurred) :
            print("There has to be only one face")
        # else:
        #     showEllipse(img)
    # dfs = DeepFace.find(img_path=img, db_path="C:/Users/akhme/Desktop/diploma/images", model_name='Facenet')
    # face = DeepFace.detectFace(img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("exit")
        break

    if cv2.waitKey(1) & 0xFF == ord('t'):
        print("taken")
        takePhoto('image' + str(rd.randint(1, 1500000)) + '.png', img)
        break
    
    cv2.imshow("Image", img)


cap.release()
