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
    "19B030222": {
        "firstname": "Tomiris",
        "middlename": "Ustudy",
        "lastname": "Baktybayeva",
        "faculty": "IT",
        "major": "CSS",
        "starting_year": 2019,
        # "total_attendance": 7,
        # "standing": "G",
        # "year": 4,
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
        # "year": 4,
        # "last_attendance_time": "2022-12-11 00:54:34"
    },
}


# print(len(student))
for key, value in data.items():
    # ref.push(data["19B030291"])
    print(key, value)

# sorted = ref.order_by_child("enter_time").get()
# ref.push(data['19B030291'])

# count = 0
# sorted = list(sorted.items())[::-1]
# print(sorted[0][1])
# for k in list(sorted.items())[::-1]:
    # print(k[1]['enter_time'])

    # exited = 'enter'
    # if k[1]["enter_or_exit"] == 'enter':
    #     exited = 'exit'
    # else: exited = 'enter'
    # count += 1
    # if count == 1:
    #     ref.push({
    #         "id": k[1]['id'],
    #         "firstname": k[1]['firstname'],
    #         "middlename": k[1]['middlename'],
    #         "lastname": k[1]['lastname'],
    #         "faculty": k[1]['faculty'],
    #         "major": k[1]['major'],
    #         "starting_year": k[1]['starting_year'],
    #         "enter_time": f'{datetime.datetime.now()}',
    #         "enter_or_exit": exited,
    #         # "total_attendance": 7,
    #         # "standing": "G",
    #         "year": k[1]['year'],
    #         # "last_attendance_time": "2022-12-11 00:54:34"
    #     })
    # for key, value in k:
        # print(value['enter_time'])
# print(sorted)