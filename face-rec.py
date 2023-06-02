import cv2
import face_recognition
from deepface import DeepFace
import os
from mtcnn import MTCNN
import random as rd
import time


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2180)


img_path = r"/Users/baktybayevatomiris/Desktop/face/images"
#img_path = r"C:\\Users\\akhme\\Desktop\\diploma"
os.chdir(img_path)


square_start, square_end = (440, 100), (840, 650)

square_x = square_start[0]
square_y = square_start[1]

square_width = square_end[0] - square_x
square_height = square_end[1] - square_y


def takePhoto(path: str, img: any):
    if isUnique(path):
        cv2.imwrite(path, img)
        # cv2.destroyAllWindows()


def deletePhoto(path):
    os.remove(img_path + "\\" + path)


def isUnique(img):
    unique = True
    for file in os.listdir(img_path):
        if img == file:
            unique = False
    return unique


def showEllipse(img, locations, show=True):
    count = 0
    if len(locations) == 1:
        (top, right, bottom, left) = locations[0]

        print("Face")
        croppedTook = img[
            square_y : square_y + square_height,
            square_x : square_x + square_width,
        ]
        cv2.imshow("CroppedTook", croppedTook)

        isTaken = False
        isFound = None
        try:
            randId = rd.randint(1, 1500000)
            if count == 0:
                takePhoto("deleted/image" + str(randId) + ".png", croppedTook)
                count += 1
                isTaken = True
                time.sleep(3)
            print(count, os.path.exists("deleted/image" + str(randId) + ".png"), randId)
            if count == 1 and os.path.exists("deleted/image" + str(randId) + ".png"):
                took = cv2.imread("deleted/image" + str(randId) + ".png")
                dfs = DeepFace.extract_faces(croppedTook)
                width, height = (
                    dfs[0]["facial_area"]["w"],
                    dfs[0]["facial_area"]["h"],
                )
                size = width * height
                distance = 100 / (size**0.5)
                if int(distance * 100) > 30:
                    print("far")
                else:
                    print("suits")
                    isFound = True
                print(size, distance)
                # cv2.destroyAllWindows()
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
        faceErrorText = "Face not found"
        faceFoundText = "Face found"
        warningTextXY = (50, 680)
        errorTextXY = (550, 680)
        foundTextXY = (750, 680)
        thickness = 1

        withText = cv2.putText(
            squareImg,
            warningText,
            warningTextXY,
            font,
            0.6,
            (0, 255, 0),
            thickness,
            cv2.LINE_AA,
        )
        errorText = cv2.putText(
            squareImg,
            faceErrorText,
            errorTextXY,
            font,
            0.6,
            (0, 0, 250),
            thickness,
            cv2.LINE_AA,
        )

        foundText = cv2.putText(
            squareImg,
            faceFoundText,
            foundTextXY,
            font,
            0.6,
            (250, 0, 0),
            thickness,
            cv2.LINE_AA,
        )
    else:
        print("Many items")
    cv2.imshow("Video", img)


# def isOnePerson(img: any) -> bool:
#     detector = MTCNN()
#     detections = detector.detect_faces(img)
#     print("Length", len(detections))
#     return len(detections) == 1


while True:
    ret, frame = cap.read()

    # rgb_frame = frame[:, :, ::-1]

    # face_locations = face_recognition.face_locations(frame)

    # for top, right, bottom, left in face_locations:
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    mirrored_img = cv2.flip(frame, 1)

    showEllipse(mirrored_img, [], True)
    # cv2.imshow("Video", mirrored_img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Освобождение ресурсов
cap.release()
# cv2.destroyAllWindows()

# len(face_located) == 1 and left >= square_x and left < square_end[0] and right > square_x and right <= square_end[0] and top >= square_start[1] and top < square_end[1] and bottom <= square_end[1] and bottom > square_start[1]
