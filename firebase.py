import firebase_admin
from firebase_admin import credentials, db, storage
import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://face-atendance-default-rtdb.europe-west1.firebasedatabase.app/"
    },
)


ref = db.reference("sessions")
refPer = db.reference('persons')

student = ref.get()

# print(student)


data = {
    # "19B030068": {
    #     "firstname": "Assan",
    #     "middlename": "Nurlan",
    #     "lastname": "Akhmetov",
    #     "faculty": "IT",
    #     "major": "IS",
    #     "starting_year": 2019,
    #     # "total_attendance": 7,
    #     # "standing": "G",
    #     "year": 4,
    #     # "last_attendance_time": "2022-12-11 00:54:34"
    # },
    # "19B030291": {
    #     "id": "19B030291",
    #     "firstname": "Assylgul",
    #     "middlename": "Altynbek",
    #     "lastname": "Janayeva",
    #     "faculty": "IT",
    #     "major": "CSS",
    #     "starting_year": 2019,
    #     "enter_time": f'{datetime.datetime.now()}',
    #     # "enter_or_exit": "enter" if student and student['enter_or_exit'] == "enter" else "exit" if student and student['enter_or_exit'] == "exit" else "enter",
    #     "enter_or_exit": "enter",
    #     # "total_attendance": 7,
    #     # "standing": "G",
    #     "year": 4,
    #     # "last_attendance_time": "2022-12-11 00:54:34"
    # },
    # "19B030222": {
    #     "firstname": "Tomiris",
    #     "middlename": "Ustudy",
    #     "lastname": "Baktybayeva",
    #     "faculty": "IT",
    #     "major": "CSS",
    #     "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        # "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    # },
    # "19B030067": {
    #     "firstname": "Damir",
    #     "middlename": "Oraz",
    #     "lastname": "Yessenbek",
    #     "faculty": "IT",
    #     "major": "IS",
    #     "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        # "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    # },
    "15M030069":{
        "degree": "Bachelor",
        "faculty": "01",
        "firstname":"Vladimir",
        "lastname": "Popov",
        "major": "IS",
        "middlename": "Unknown",
        "sex": "M",
        "starting_year":2015
    },
    "19B030067":{
        "degree": "Bachelor",
        "faculty": "01",
        "firstname":"Damir",
        "lastname": "Yessenbek",
        "major": "IS",
        "middlename": "Oraz",
        "sex": "M",
        "starting_year":2019
    },
    "19B030068":{
        "degree": "Bachelor",
        "faculty": "01",
        "firstname":"Assan",
        "lastname": "Akhmetov",
        "major": "IS",
        "middlename": "Nurlan",
        "sex": "M",
        "starting_year":2019
    },
    "19B030222":{
        "degree": "Bachelor",
        "faculty": "01",
        "firstname":"Tomiris",
        "lastname": "Baktybayeva",
        "major": "IS",
        "middlename": "Beyimbet",
        "sex": "F",
        "starting_year":2019
    },
    "19B030291":{
        "degree": "Bachelor",
        "faculty": "01",
        "firstname":"Assylgul",
        "lastname": "Janayeva",
        "major": "IS",
        "middlename": "Altynbek",
        "sex": "F",
        "starting_year":2019
    }
}

for key, value in data.items():
    refPer.child(key).set(value)
    # print(key, value)