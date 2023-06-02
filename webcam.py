import cv2
from deepface import DeepFace
import face_recognition as fc
import firebase_admin
from firebase_admin import credentials as crd
from firebase_admin import storage, db

from google.cloud import storage as strg
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('serviceAccountKey.json')
client = strg.Client(credentials=credentials, project='face-atendance')

# if not firebase_admin._apps:
cred = crd.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'face-atendance.appspot.com',
    "databaseURL": "https://face-atendance-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Open the default camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

square_start, square_end = (440, 100), (840, 650)

square_x = square_start[0]
square_y = square_start[1]

square_width = square_end[0] - square_x
square_height = square_end[1] - square_y


def showEllipse(img, show=True):
    new_img = img
    count = 0
    # try:
    isTaken = False
    isFound = None
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
            # print("far")
            isFound = "Closer"
            count = 0
        else:
            # print("suits")
            isFound = True
            count = 1
        # print(dfs, size, distance)
    except:
        # print("ustudy")
        count = 0
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
    nameSurnameTextXY = (250, 680)
    errorTextXY = (550, 680)
    foundTextXY = (750, 680)
    thickness = 1


    if isFound == None or isFound == False:
        ellipsedImg = cv2.ellipse(
        img, (640, 360), (300, 200), 90, 0, 360, (0, 0, 255), 5
    )
        cv2.putText(
            squareImg,
            warningText,
            warningTextXY,
            font,
            0.6,
            (0, 0, 255),
            thickness,
            cv2.LINE_AA,
        )
    elif isFound == "Closer":
        ellipsedImg = cv2.ellipse(
        img, (640, 360), (300, 200), 90, 0, 360, (250, 0, 0), 5
    )
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
        if count == 1 and cv2.waitKey(1) & 0xFF == ord('k'):
            # print("K dzhigi")
            foundFace = DeepFace.find(img, db_path="deleted", model_name="VGG-Face", enforce_detection=False)
            img_path_extracted = foundFace[0].iloc[0]['identity']
            if img_path_extracted.count('deleted') > 0:
                img_id = img_path_extracted.split("/")[1].split(".")[0]
            else:
                img_id = img_path_extracted.split("/")[1].split(".")[0]
            print(img_path_extracted, img_id)
            # print(img_id)

            isNotDetected = False
            try:
                # DeepFace.extract_faces(img_path1)
                verified = DeepFace.verify(img, img_path_extracted, model_name="VGG-Face", enforce_detection=False)
                print(verified)
                # if verified['verified']:
                #     # print(verified)
                #     isNotDetected = False
                #     print("Detected", verified)
                # else: 
                #     print("Not detected")
            except:
                isNotDetected = True
                # print("Face is not detected")

            if isNotDetected:
                sadas = 1
                print("Rodnoi, no way")
            else:
                ref = db.reference('persons')
                # print(ref)
                data = ref.child(img_id).get()
                cv2.putText(
                    squareImg,
                    data['firstname'] + ' ' + data['lastname'],
                    nameSurnameTextXY,
                    font,
                    0.6,
                    (0, 250, 0),
                    thickness,
                    cv2.LINE_AA,
                )
                cv2.imshow("Name Surname", img)
                print(data['firstname'], data['lastname'])
                # print(verified)

            # print(count, "Identifying", foundFace)
    cv2.imshow("Dzhigi", img)
    # except:
    #     print("Maybe error?")

while True:
    # Read a new frame from the camera
    ret, img = cap.read()
    mirrored_img = cv2.flip(img, 1)

    # Display the resulting frame
    # try:
    showEllipse(mirrored_img)
    # except:
    #     print("not found")
    # cv2.imshow('Webcam', mirrored_img)

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

# arch -arm64 python3
# python3-intel64