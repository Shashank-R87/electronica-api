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

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]

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