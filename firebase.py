import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://face-atendance-default-rtdb.europe-west1.firebasedatabase.app/"
    },
)


ref = db.reference("persons")

data = {
    "19B030068": {
        "firstname": "Assan",
        "middlename": "Nurlan",
        "lastname": "Akhmetov",
        "faculty": "IT",
        "major": "IS",
        "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    },
    "19B030291": {
        "firstname": "Assylgul",
        "middlename": "Altynbek",
        "lastname": "Janayeva",
        "faculty": "IT",
        "major": "CSS",
        "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    },
    "19B030222": {
        "firstname": "Tomiris",
        "middlename": "Ustudy",
        "lastname": "Baktybayeva",
        "faculty": "IT",
        "major": "CSS",
        "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    },
    "19B030067": {
        "firstname": "Damir",
        "middlename": "Oraz",
        "lastname": "Yessenbek",
        "faculty": "IT",
        "major": "IS",
        "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    },
}


for key, value in data.items():
    ref.child(key).set(value)
