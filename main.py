import cv2
import random as rd
import os
from deepface import DeepFace
import numpy as np
import time

import face_recognition as fc
from mtcnn import MTCNN

# cv2.Vide
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1120)


img_path = r"C:\\Users\\akhme\\Desktop\\diploma\\images"
os.chdir(img_path)


square_start, square_end = (440, 100), (840, 650)

square_x = square_start[0]
square_y = square_start[1]

square_width = square_end[0] - square_x
square_height = square_end[1] - square_y


def takePhoto(path: str, img: any):
    if isUnique(path):
        cv2.imwrite(path, img)
        cv2.destroyAllWindows()


def deletePhoto(path):
    os.remove(img_path + "\\" + path)


def isUnique(img):
    unique = True
    for file in os.listdir(img_path):
        if img == file:
            unique = False
    return unique


def showEllipse(img, show=True):
    new_img = img
    # face_located = fc.face_locations(img)

    try:
        isTaken = False
        isFound = None

        # if cv2.waitKey(1) & 0xFF == ord("z"):
        # randId = rd.randint(1, 1500000)
        # takePhoto("image" + str(randId) + ".png", img)
        # isTaken = True

        # if isTaken and os.path.exists("image" + str(randId) + ".png"):
        # took = cv2.imread("image" + str(randId) + ".png")
        # croppedTook = took[
        #     square_y : square_y + square_height,
        #     square_x : square_x + square_width,
        # ]
        # cv2.imshow("CroppedTook", croppedTook)

        try:
            dfs = DeepFace.extract_faces(img)
            isFound = True
            width, height = (
                dfs[0]["facial_area"]["w"],
                dfs[0]["facial_area"]["h"],
            )
            size = width * height
            distance = 100 / (size**0.5)
            if int(distance * 100) > 30:
                print("far")
                isFound = "Closer"
            else:
                print("suits")
                isFound = True
            # print(dfs, size, distance)
        except:
            print("ustudy")
            isFound = False

        ellipsedImg = cv2.ellipse(
            img, (640, 360), (300, 200), 90, 0, 360, (0, 255, 0), 5
        )
        squareImg = cv2.rectangle(
            ellipsedImg, (440, 100), (840, 650), (125, 125, 125), 2
        )
        # green_image = cv2.cvtColor(image, cv2.C)
        font = cv2.FONT_HERSHEY_COMPLEX
        warningText = "Лицо должно быть в области эллипса"
        faceErrorText = "Лицо не найдено"
        faceFoundText = "Лицо найдено"
        closerFaceText = "Встаньте ближе"
        warningTextXY = (50, 680)
        errorTextXY = (550, 680)
        foundTextXY = (750, 680)
        thickness = 1

        print(isFound)
        if isFound == None or isFound == False:
            cv2.putText(
                squareImg,
                warningText,
                warningTextXY,
                font,
                0.6,
                (0, 0, 0),
                thickness,
                cv2.LINE_AA,
            )

            # cv2.imshow("Face Attendace2", img)
        elif isFound == "Closer":
            cv2.putText(
                squareImg,
                closerFaceText,
                warningTextXY,
                font,
                0.6,
                (250, 0, 0),
                thickness,
                cv2.LINE_AA,
            )
            # cv2.imshow("Face Attendace Closer", img)
        else:
            cv2.putText(
                squareImg,
                faceFoundText,
                warningTextXY,
                font,
                0.6,
                (0, 250, 0),
                thickness,
                cv2.LINE_AA,
            )
            # cv2.imshow("Face Attendace3", img)
        cv2.imshow("Dzhigi", img)
    except:
        print("many faces")


def isOnePerson(img: any) -> bool:
    detector = MTCNN()
    detections = detector.detect_faces(img)
    print("Length", len(detections))
    return len(detections) == 1


while True:
    success, img = cap.read()
    mirrored_img = cv2.flip(img, 1)
    # if cv2.waitKey(1) & 0xFF == ord('o'):
    #     print("clicked")
    #     if not isOnePerson(face_blurred) :
    #         print("There has to be only one face")
    # else:
    #     showEllipse(img)
    # dfs = DeepFace.find(img_path=img, db_path="C:/Users/akhme/Desktop/diploma/images", model_name='Facenet')
    edited_img = mirrored_img
    try:
        showEllipse(mirrored_img)
    except:
        print("not found")

    # cv2.imshow("Image", mirrored_img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("exit")
        break

    if cv2.waitKey(1) & 0xFF == ord("t"):
        print("taken")
        takePhoto("image" + str(rd.randint(1, 1500000)) + ".png", img)
        break

    # cv2.imshow("Image", mirrored_img)


cap.release()
