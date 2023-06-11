import cv2
from deepface import DeepFace
from deepface.basemodels import VGGFace
import face_recognition 
import firebase_admin
from firebase_admin import credentials as crd
from firebase_admin import storage, db
import numpy as np
from google.cloud import storage as strg
from google.oauth2 import service_account
import os
import datetime
from pyfirmata import Arduino, SERVO, OUTPUT
import serial.tools.list_ports
import random as rd
import time
from playsound import playsound


# ports = serial.tools.list_ports.comports()


# for port in ports:
#     print(port.device)

# board = Arduino('/dev/cu.usbmodem1101')

# servo_pin = 13
# servo = board.get_pin('d:{}:s'.format(servo_pin))
# print(servo, board)
# green_led_pin = 8
# red_led_pin = 9
# buzzer_pin = 12

# board.digital[green_led_pin].mode = OUTPUT
# board.digital[red_led_pin].mode = OUTPUT
# board.digital[buzzer_pin].mode = OUTPUT
# board.digital[servo_pin].mode = SERVO

model = VGGFace.loadModel()


credentials = service_account.Credentials.from_service_account_file('serviceAccountKey.json')
client = strg.Client(credentials=credentials, project='face-atendance')

cred = crd.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'face-atendance.appspot.com',
    "databaseURL": "https://face-atendance-default-rtdb.europe-west1.firebasedatabase.app/"
})

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

square_start, square_end = (440, 100), (840, 650)

square_x = square_start[0]
square_y = square_start[1]

square_width = square_end[0] - square_x
square_height = square_end[1] - square_y

def findEncodings(images):
  encodeList = []
  for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
    return encodeList
  
path = 'db'
images = []
myList = os.listdir(path)
classNames = []
for cl in myList:
    # print(cl)
    if os.path.isdir(f'{path}/{cl}'):
        # print(True)
       for filename in os.listdir(f'{path}/{cl}'):
        if filename.count('.png'):
            curImg = cv2.imread(f'{path}/{cl}/{filename}')
            images.append(curImg)
            # classNames.append(os.path.splitext(filename)[0])
            classNames.append(f'{path}/{cl}/{filename}')
    # else:
        # curImg = cv2.imread(f'{path}/{cl}')
        # images.append(curImg)
        # classNames.append(os.path.splitext(cl)[0])
        # print(classNames)


img_path = r"/Users/baktybayevatomiris/Desktop/face/images"
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

encodeListKnown = findEncodings(images)

last_time = datetime.datetime.now()

def showEllipse(img, show=True):
    count = 0
    countPush = 0
    isTaken = False
    isFound = None
    try:
        dfs = DeepFace.extract_faces(img[square_start[1]: square_start[1] + 550, square_start[0]: square_start[0] + 400])
        # isFound = True
        width, height = (
            dfs[0]["facial_area"]["w"],
            dfs[0]["facial_area"]["h"],
        )
        size = width * height
        distance = 100 / (size**0.5)
        if int(distance * 100) > 30:
            isFound = "Closer"
            count = 0
        elif int(distance * 100) < 20:
            isFound = "Farther"
            count = 0
        else:
            isFound = True
            count = 1
    except:
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
    fatherFaceText = "Будьте на расстоянии 15 см"
    notFoundFaceErrorText = "Лицо не найдено в базе данных"

    warningTextXY = (50, 680)
    nameSurnameTextXY = (450, 680)
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
    elif isFound == "Farther":
        ellipsedImg = cv2.ellipse(
            img, (640, 360), (300, 200), 90, 0, 360, (250, 0, 170), 5
        )
        cv2.putText(
            squareImg,
            fatherFaceText,
            warningTextXY,
            font,
            0.6,
            (250, 0, 170),
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
        if count == 1 :
            try:
                foundFace = DeepFace.find(img, db_path='/Users/baktybayevatomiris/Desktop/face/db', model_name="Facenet")
                # print("FOUNDFACE", foundFace)
                if len(foundFace) > 0: 
                    img_path_extracted = foundFace[0].iloc[0]['identity']
                    if img_path_extracted.count(path) > 0:
                        img_id = img_path_extracted.split(path)[1].split(".")[0].split('/')[1]

                    print(img_id)

                    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                    facesCurFrame = face_recognition.face_locations(imgS)
                    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

                    isNotDetected = False
                    print(img_path_extracted)
                    try:
                        verified = DeepFace.verify(img, img_path_extracted)
                        verified_facenet = DeepFace.verify(img, img_path_extracted, model_name='Facenet')
                        analyze = DeepFace.analyze(img)
                        matches = []
                        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                            #print(faceDis)
                            matchIndex = np.argmin(faceDis)
                        
                        print(
                            "VGG-FACE", verified['distance'], '\n',
                            "FACENET", verified_facenet['distance'], '\n', 
                            # 'ArcFace', verified_arcface['distance'], '\n',
                            'Gender', analyze[0]['dominant_gender'], '\n',
                            # matches, matchIndex,
                            # matches[matchIndex],
                            verified_facenet['distance']*100, '\n',verified['distance']*100
                            )
                        
                        if verified['verified'] and int(verified_facenet['distance']*100) in range(-20, 24) and int(verified['distance']*100) in range(-20, 24) and verified_facenet['verified']:
                            # print(verified, matches)
                            print("True")
                            isNotDetected = False
                        else: 
                            isNotDetected = True
                            print("Not detected")
                            # board.digital[red_led_pin].write(1)
                            # board.pass_time(2)
                            # playsound('media/access-denied.mp4')
                            # board.digital[red_led_pin].write(0)
                    except:
                        isNotDetected = True
                        # board.digital[buzzer_pin].write(12, 569, 2000)
                       # board.digital[red_led_pin].write(1)
                        # print("Face is not detected")
                        playsound('/Users/baktybayevatomiris/Desktop/face/media/access-denied.mp4')
                        # board.pass_time(1)
                        # board.digital[red_led_pin].write(0)
                        

                    if not isNotDetected:
                        ref = db.reference('persons')
                        sessionsRef = db.reference('sessions')
                        data = ref.child(img_id).get()
                        sorted = sessionsRef.order_by_child("enter_time").get()
                        sorted = list(sorted.items())[::-1]
                        studentData = sorted[0]
                        
                        # board.digital[buzzer_pin].write(1)
                        #board.digital[buzzer_pin].write(12, 120, 2000)
                        #board.pass_time(2)
                        print("Goes on")
                        if len(sorted) > 0:
                            studentEnter_Exit = sorted[0][1]['enter_or_exit']
                            if studentEnter_Exit == "enter":
                                studentEnter_Exit = "exit"
                            else:
                                studentEnter_Exit = "enter"
                            countPush += 1
                            if countPush == 1 and ((data['sex'] == 'F' and analyze[0]['dominant_gender'] == 'Woman') or (data['sex'] == 'M' and analyze[0]['dominant_gender'] == 'Man')):
                                sessionsRef.push({
                                    # "id": studentData['id'],
                                    "id": img_id,
                                    "firstname": data['firstname'],
                                    "middlename": data['middlename'],
                                    "lastname": data['lastname'],
                                    "faculty": data['faculty'],
                                    "major": data['major'],
                                    "starting_year": data['starting_year'],
                                    "enter_time": f'{datetime.datetime.now()}',
                                    "enter_or_exit": studentEnter_Exit,
                                    "starting_year": data['starting_year']
                                })
                                
                        datetime_detected = datetime.datetime.now()
                        if (data['sex'] == 'F' and analyze[0]['dominant_gender'] == 'Woman') or (data['sex'] == 'M' and analyze[0]['dominant_gender'] == 'Man'):
                            # board.digital[green_led_pin].write(1)
                            # board.digital[servo_pin].write(90)
                            print(data['firstname'], data['lastname'])
                            if data['firstname'] == 'Vladimir':
                                playsound('/Users/baktybayevatomiris/Desktop/face/media/popi.mp4')
                            elif data['firstname'] == "Alimzhan" and data['lastname'] == "Amanov":
                                playsound('/Users/baktybayevatomiris/Desktop/face/media/welcome-amanov.mp4')
                            else:
                                playsound('/Users/baktybayevatomiris/Desktop/face/media/access-granted.mp4')
                            time.sleep(2)
                            # board.digital[green_led_pin].write(0)
                            # board.digital[servo_pin].write(0)
                        else:
                            isNotDetected = True
                        # board.digital[buzzer_pin].write(0)
                    else:
                        # board.digital[red_led_pin].write(1)
                        # board.pass_time(1)
                        playsound('/Users/baktybayevatomiris/Desktop/face/media/access-denied.mp4')
                       # board.digital[red_led_pin].write(0)

            except: 
                print("Some error")
                # board.digital[red_led_pin].write(1)
                # board.pass_time(1)
                playsound('/Users/baktybayevatomiris/Desktop/face/media/access-denied.mp4')
                #board.digital[red_led_pin].write(0)
    cv2.imshow("Dzhigi", img)


while True:

    ret, img = cap.read()
    mirrored_img = cv2.flip(img, 1)

    showEllipse(mirrored_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if cv2.waitKey(1) & 0xFF == ord("t"):
        print("taken")
        takePhoto("image" + str(rd.randint(1, 1500000)) + ".png", img)
        break

cap.release()
cv2.destroyAllWindows()

# arch -arm64 python3
# python3-intel64