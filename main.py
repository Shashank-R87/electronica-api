#FIREBASE
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db

#GOOGLE SHEETS
from google.oauth2 import service_account
from googleapiclient.discovery import build

#FASTAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import random

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cred = credentials.Certificate("electronica-39be5-e9d58c7bd0e6.json")
credentials = service_account.Credentials.from_service_account_file(
    "electronica-39be5-e9d58c7bd0e6.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
firebase_admin.initialize_app(cred,{
    "databaseURL": "https://electronica-39be5-default-rtdb.asia-southeast1.firebasedatabase.app"
})

service = build("sheets", "v4", credentials=credentials)
SHEET_ID = "1nDCV7RCrKIk5vmAPX19pCUV3h9Gq9pb3IYySdZHl1HU"

@app.get("/setPayment/{id}")
def setPayment(id:str):
    ref = db.reference(f"users/{id}")
    try:
        ref.set({
            "teamAvailable": True,
            "paymentDone": True,
            "paymentVerified": False
            })
        return 200
    except:
        return 400

@app.get("/setNewUser/{id}")
def setNewUser(id:str):
    ref = db.reference(f"users/{id}")

    try:
        ref.set({
            "teamAvailable": False,
            "paymentDone": False,
            "paymentVerified": False
            })
        return 200
    except:
        return 400
    
@app.get("/getTeam/{id}")
def getTeam(id: str):
    result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="Teams").execute()
    for i in result["values"]:
        if i[0]==id:
            return {"teamname": i[1], 
                    "id": i[0],
                    
                    "leader": i[2], 
                    "leaderReg": i[3].split('-')[0], 

                    "member1": i[6], 
                    "member1Reg": i[7].split("-")[0], 

                    "member2": i[9],
                    "member2Reg": i[10].split("-")[0],

                    "member3": i[12], 
                    "member3Reg": i[13].split("-")[0]}

@app.get("/basics/{id}")
def getBasics(id:str):
    ref = db.reference(f"users/{id}")
    try:
        result = ref.get()
        return result
    except:
        return 400
    
@app.put("/setTeam/{id}")
async def setTeam(id: str, request: Request):
    data = await request.json()
    body_data = [[
            id,
            data["data"]["teamname"], 
            data['leader']['leaderName'].title(), 
            data['leader']['leaderReg']+" - "+data["data"]["section"][0],
            data['data']['genders'][0]+" - "+data['data']['residency'][0],
            data['data']["contact"],

            data['data']['members'][0].title(), 
            data['data']['member_reg'][0]+" - "+data["data"]["section"][1],
            data['data']['genders'][1]+" - "+data['data']['residency'][1],

            data['data']['members'][1].title(), 
            data['data']['member_reg'][1]+" - "+data["data"]["section"][2],
            data['data']['genders'][2]+" - "+data['data']['residency'][2],  
            
            data['data']['members'][2].title(), 
            data['data']['member_reg'][2]+" - "+data["data"]["section"][3],
            data['data']['genders'][3]+" - "+data['data']['residency'][3], False],]
    body = {"values": body_data}

    try:
        result = service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range="Teams", valueInputOption="USER_ENTERED", body=body).execute()
        ref = db.reference(f"/users/{id}")
        ref.set({
            "paymentDone": False,
            "paymentVerified": False,
            "teamAvailable": True
        })
        return 200
    except:
        return 400


#EVENT

@app.get("/getMisc")
def getMisc():
    ref = db.reference("/misc")
    return ref.get()

@app.get("/getQuestions")
def getQuestions():
    questions = [{
        "id": 1,
        "question": "Which sensor is used for calculating distance?",
        "options": ["IR Sensor", "Ultrasonic Sensor", "PIR Sensor", "LDR Sensor"]
    },
    {
        "id": 2,
        "question": "Which sensor is used for adjusting brightness of light automatically?",
        "options": ["IR Sensor", "Ultrasonic Sensor", "PIR Sensor", "LDR Sensor"]
    },
    {
        "id": 3,
        "question": "Which sensor is used for detecting black and white colors?",
        "options": ["IR Sensor", "Ultrasonic Sensor", "PIR Sensor", "LDR Sensor"]
    },
    {
        "id": 4,
        "question": "Which sensor is used for detecting motion?",
        "options": ["IR Sensor", "Ultrasonic Sensor", "PIR Sensor", "LDR Sensor"]
    },
    {
        "id": 5,
        "question": "Which diode is used as a light source?",
        "options": ["LED", "1N4007", "LDR", "PIR"]
    },
    {
        "id": 6,
        "question": "If 1 and 0 are given as inputs to an AND gate what's the output?",
        "options": ["1", "0", "None", "Both"]
    },
    ]
    random.shuffle(questions)
    return questions

@app.put("/submitRound1/{id}")
async def submitRound1(id: str, request: Request):
    answer = {'1': '2', '2': '4', '3': '1', '4': '3', '5': '1', '6': '2'}
    result = await request.json()
    round1c = result["round1c"]
    
    score = 0
    if (round1c!=answer):
        for i in round1c:
            if round1c[i] == answer[i]:
                score+=1
    else:
        score = 6

    body = {'values': [[id, result["teamName"], 0, 0, score, result["round1a"], f"{round1c}"]]}
    result = service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range="Round1", valueInputOption="USER_ENTERED", body=body).execute()

@app.get("/round1Check/{id}")
def round1Check(id: str):
    result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="Round1").execute()
    data = result['values']
    for i in data:
        if  i[0]==id:
            return 200
    return 404

@app.get("/getround2/{id}/{teamName}")
def getRound2(id: str, teamName: str):
    result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="Round2").execute()
    data = result['values']

    questionPresent = False
    for i in data:
        if i[0] == id:
            questionPresent = True
            return [i[2], i[3], i[4]]

    if not questionPresent:
        hardQuestions = [f"Hard Question {i}" for i in range(1, 11)]
        mediumQuestionsSet1 = [f"Medium Question {i} from Set 1" for i in range(1, 11)]
        mediumQuestionsSet2 = [f"Medium Question {i} from Set 2" for i in range(1, 11)]
        questions = [hardQuestions[random.randint(0, 9)], mediumQuestionsSet1[random.randint(0, 9)], mediumQuestionsSet2[random.randint(0, 9)]]
        body = {'values': [[id, teamName, questions[0], questions[1], questions[2]]]}
        result = service.spreadsheets().values().append(spreadsheetId=SHEET_ID, range="Round2", valueInputOption="USER_ENTERED", body=body).execute()
        return questions
