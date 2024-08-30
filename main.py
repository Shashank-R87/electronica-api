# FIREBASE
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# GOOGLE SHEETS
from google.oauth2 import service_account
from googleapiclient.discovery import build

# FASTAPI
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
    "electronica-39be5-e9d58c7bd0e6.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://electronica-39be5-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)

service = build("sheets", "v4", credentials=credentials)
SHEET_ID = "1nDCV7RCrKIk5vmAPX19pCUV3h9Gq9pb3IYySdZHl1HU"


@app.get("/setPayment/{id}")
def setPayment(id: str):
    ref = db.reference(f"users/{id}")
    try:
        ref.set({"teamAvailable": True, "paymentDone": True, "paymentVerified": False})
        return 200
    except:
        return 400


@app.get("/setNewUser/{id}")
def setNewUser(id: str):
    ref = db.reference(f"users/{id}")

    try:
        ref.set(
            {"teamAvailable": False, "paymentDone": False, "paymentVerified": False}
        )
        return 200
    except:
        return 400


@app.get("/getTeam/{id}")
def getTeam(id: str):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range="Teams")
        .execute()
    )
    for i in result["values"]:
        if i[0] == id:
            return {
                "teamname": i[1],
                "id": i[0],
                "leader": i[2],
                "leaderReg": i[3].split("-")[0],
                "member1": i[6],
                "member1Reg": i[7].split("-")[0],
                "member2": i[9],
                "member2Reg": i[10].split("-")[0],
                "member3": i[12],
                "member3Reg": i[13].split("-")[0],
            }


@app.get("/basics/{id}")
def getBasics(id: str):
    ref = db.reference(f"users/{id}")
    try:
        result = ref.get()
        return result
    except:
        return 400


@app.put("/setTeam/{id}")
async def setTeam(id: str, request: Request):
    data = await request.json()
    body_data = [
        [
            id,
            data["data"]["teamname"],
            data["leader"]["leaderName"].title(),
            data["leader"]["leaderReg"] + " - " + data["data"]["section"][0],
            data["data"]["genders"][0] + " - " + data["data"]["residency"][0],
            data["data"]["contact"],
            data["data"]["members"][0].title(),
            data["data"]["member_reg"][0] + " - " + data["data"]["section"][1],
            data["data"]["genders"][1] + " - " + data["data"]["residency"][1],
            data["data"]["members"][1].title(),
            data["data"]["member_reg"][1] + " - " + data["data"]["section"][2],
            data["data"]["genders"][2] + " - " + data["data"]["residency"][2],
            data["data"]["members"][2].title(),
            data["data"]["member_reg"][2] + " - " + data["data"]["section"][3],
            data["data"]["genders"][3] + " - " + data["data"]["residency"][3],
            False,
        ],
    ]
    body = {"values": body_data}

    try:
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SHEET_ID,
                range="Teams",
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        ref = db.reference(f"/users/{id}")
        ref.set({"paymentDone": False, "paymentVerified": False, "teamAvailable": True})
        return 200
    except:
        return 400


# EVENT


@app.get("/getMisc")
def getMisc():
    ref = db.reference("/misc")
    return ref.get()


@app.get("/getQuestions")
def getQuestions():
    questions = [
        {
            "id": 1,
            "question": "Which of the following sensors typically requires a library to interface with Arduino?",
            "options": [
                "Photoresistor",
                "LM35 Temperature Sensor",
                "HC-SR04 Ultrasonic Sensor",
                "MPU6050 Gyroscope/Accelerometer",
            ],
        },
        {
            "id": 2,
            "question": "In an I2C communication setup, which pins are used for the data and clock signals on an Arduino Uno?",
            "options": ["A0 and A1", "D2 and D3", "A4 and A5", "D10 and D11"],
        },
        {
            "id": 3,
            "question": "What is the primary advantage of using an interrupt with a sensor in an Arduino project?",
            "options": [
                "Reduces the power consumption of the Arduino",
                "Allows the sensor to operate at a higher speed",
                "Enables the Arduino to respond immediately to events without polling",
                "Increases the number of sensors that can be connected",
            ],
        },
        {
            "id": 4,
            "question": "What type of sensor is the HC-SR04?",
            "options": [
                "Temperature Sensor",
                "Pressure Sensor",
                "Ultrasonic Distance Sensor",
                "Light Sensor",
            ],
        },
        {
            "id": 5,
            "question": "What is the typical purpose of an analog-to-digital converter (ADC) in an IoT sensor system?",
            "options": [
                "Convert digital signals to analog for sensor communication",
                "Increase the range of analog sensors",
                "Convert analog signals from sensors into digital data for processing",
                "Amplify analog signals for better resolution",
            ],
        },
        {
            "id": 6,
            "question": "Which of the following is a key consideration when implementing a low-power IoT sensor node that operates on a battery for extended periods?",
            "options": [
                "High data transmission rates",
                "Frequent data sampling",
                "Power-efficient data transmission and sleep modes",
                "High processing power",
            ],
        },
        {
            "id": 7,
            "question": "Which of the following sensors can measure both temperature and humidity in an IoT system?",
            "options": ["BMP280", "DHT22", "MQ-7", "HC-SR04"],
        },
        {
            "id": 8,
            "question": "What type of sensor is the TCS3200 and what is its primary use?",
            "options": [
                "Temperature Sensor, used for monitoring ambient temperature",
                "Light Sensor, used for detecting light intensity and color",
                "Pressure Sensor, used for measuring atmospheric pressure",
                "Proximity Sensor, used for measuring distances to objects",
            ],
        },
        {
            "id": 9,
            "question": "When using an MQ-135 sensor for air quality monitoring, what type of gas concentrations can it measure?",
            "options": [
                "Only carbon dioxide",
                "Only volatile organic compounds",
                "Multiple gases including carbon dioxide, ammonia, and benzene",
                "Only ozone",
            ],
        },
        {
            "id": 10,
            "question": "Which type of RFID technology does the MFRC522 sensor primarily support?",
            "options": [
                "Low-Frequency (LF) RFID",
                "High-Frequency (HF) RFID",
                "Ultra High-Frequency (UHF) RFID",
                "Microwave RFID",
            ],
        },
        {
            "id": 11,
            "question": "Which IoT component is responsible for executing tasks based on input from sensors?",
            "options": ["Actuator", "Gateway", "Microcontroller", "Power Supply"],
        },
        {
            "id": 12,
            "question": "What is the operating voltage of the Arduino Uno board?",
            "options": ["3.3V", "5V", "9V", "12V"],
        },
        {
            "id": 13,
            "question": "What is the maximum number of analog input pins available on the Arduino Uno?",
            "options": ["4", "6", "8", "10"],
        },
        {
            "id": 14,
            "question": "Which pin on the Arduino Uno board is typically used to receive serial data?",
            "options": ["Pin 1", "Pin 0", "Pin 2", "Pin 3"],
        },
        {
            "id": 15,
            "question": "Which of the following is a characteristic of the Arduino Uno?",
            "options": [
                "It has 8 digital pins.",
                "It operates at 1.8V.",
                "It has a 16 MHz clock speed.",
                "It has a built-in Wi-Fi module.",
            ],
        },
        {
            "id": 16,
            "question": "Which communication protocol is not natively supported by the Arduino Uno?",
            "options": ["I2C", "SPI", "UART", "Wi-Fi"],
        },
        {
            "id": 17,
            "question": "Which of the following is a PWM pin on the Arduino Uno?",
            "options": ["Pin 2", "Pin 3", "Pin A0", "Pin A5"],
        },
        {
            "id": 18,
            "question": "Which pin on the Arduino Uno is commonly used for the built-in LED?",
            "options": ["Pin 0", "Pin 1", "Pin 9", "Pin 13"],
        },
        {
            "id": 19,
            "question": "What is the purpose of the setup() function in an Arduino sketch?",
            "options": [
                "To define the main code logic.",
                "To initialize variables and set pin modes.",
                "To run repeatedly during the program's execution.",
                "To delay the execution of the code.",
            ],
        },
        {
            "id": 20,
            "question": "Which command is used to send data to the serial monitor in Arduino?",
            "options": [
                "Serial.write()",
                "Serial.print()",
                "Serial.read()",
                "Serial.begin()",
            ],
        },
        {
            "id": 21,
            "question": "How do you declare a global variable in Arduino?",
            "options": [
                "Inside the setup() function.",
                "Inside the loop() function.",
                "Outside of both setup() and loop().",
                "Inside a custom function.",
            ],
        },
        {
            "id": 22,
            "question": "What is the primary advantage of using an ESP8266 module in an Arduino-based IoT project?",
            "options": [
                "It provides high-speed data processing",
                "It adds Wi-Fi connectivity to the Arduino",
                "It increases the number of I/O pins available",
                "It allows the Arduino to interface with analog sensors",
            ],
        },
        {
            "id": 23,
            "question": "What does the analogRead() function in Arduino do when used in an IoT project?",
            "options": [
                "Sends data to the cloud",
                "Reads digital values from a pin",
                "Reads an analog input value from a pin and converts it to a digital value",
                "Writes a value to an analog pin",
            ],
        },
        {
            "id": 24,
            "question": "What is the role of the delay() function in an Arduino sketch, especially in IoT applications?",
            "options": [
                "To create a connection delay to the server",
                "To introduce a pause in the code execution for a specified time",
                "To synchronize data transmission between devices",
                "To reset the Arduino board",
            ],
        },
        {
            "id": 25,
            "question": "Which of the following statements correctly describes the function of a resistance box in a circuit?",
            "options": [
                "It measures the resistance of the circuit components.",
                "It provides a variable resistance to control the current in the circuit.",
                "It stores electrical charge for later use.",
                "It amplifies the current in the circuit.",
            ],
        },
        {
            "id": 26,
            "question": "What happens to the total resistance in a resistance box when two resistors are connected in parallel?",
            "options": [
                "The total resistance increases",
                "The total resistance decreases",
                "The total resistance remains the same",
                "The total resistance equals the sum of the individual resistances",
            ],
        },
        {
            "id": 27,
            "question": "How can you determine if the connections inside a resistance box are properly made and functioning correctly?",
            "options": [
                "By visually inspecting the box",
                "By measuring the resistance between the terminals with a multimeter",
                "By measuring the current through the box",
                "By checking the voltage across the resistors",
            ],
        },
        {
            "id": 28,
            "question": "Which component in an IR sensor is responsible for emitting infrared light?",
            "options": ["Photodiode", "Phototransistor", "IR LED", "Laser diode"],
        },
        {
            "id": 29,
            "question": "Which of the following is a common application of IR sensors?",
            "options": [
                "Temperature measurement",
                "Bluetooth communication",
                "Wireless charging",
                "Metal detection",
            ],
        },
        {
            "id": 30,
            "question": "What type of IR sensor uses a photodiode or phototransistor to detect IR light?",
            "options": [
                "Passive IR sensor",
                "Active IR sensor",
                "Reflective IR sensor",
                "Thermal IR sensor",
            ],
        },
    ]
    random.shuffle(questions)
    return questions


@app.put("/submitRound1/{id}")
async def submitRound1(id: str, request: Request):
    answer = {
        "1": "4",
        "2": "3",
        "3": "3",
        "4": "3",
        "5": "3",
        "6": "3",
        "7": "2",
        "8": "2",
        "9": "3",
        "10": "2",
        "11": "1",
        "12": "2",
        "13": "2",
        "14": "2",
        "15": "3",
        "16": "4",
        "17": "2",
        "18": "4",
        "19": "2",
        "20": "2",
        "21": "3",
        "22": "2",
        "23": "3",
        "24": "2",
        "25": "2",
        "26": "2",
        "27": "2",
        "28": "3",
        "29": "1",
        "30": "2",
    }
    result = await request.json()
    round1c = result["round1c"]

    score = 0
    if round1c != answer:
        for i in round1c:
            if round1c[i] == answer[i]:
                score += 1
    else:
        score = 6

    body = {"values": [[id, result["teamName"], 0, score, f"{round1c}"]]}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SHEET_ID,
            range="Round1",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )


@app.get("/round1Check/{id}")
def round1Check(id: str):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range="Round1")
        .execute()
    )
    data = result["values"]
    for i in data:
        if i[0] == id:
            return 200
    return 404


@app.get("/getround2/{id}/{teamName}")
def getRound2(id: str, teamName: str):
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range="Round2")
        .execute()
    )
    data = result["values"]

    questionPresent = False
    for i in data:
        if i[0] == id:
            questionPresent = True
            return [i[2], i[3], i[4]]

    if not questionPresent:
        hardQuestions = [
            "Design a temperature-controlled cooling system using an Arduino, a DHT11 temperature and humidity sensor, a 5V relay module, a 12V DC fan, and a 12V power supply. Include an LCD display to show the current temperature and humidity. The fan should turn on when the temperature exceeds a set threshold (e.g., 30°C) and turn off when the temperature drops below this threshold. Additionally, incorporate an emergency shutoff mechanism using a push-button, and an LED to indicate whether the system is active or in emergency mode.",
            "Create a system where a laser-based security alarm is activated when the laser beam is interrupted, and the alarm can only be turned off by entering a code on the keypad? The system should also control an external device via the relay, triggered by specific keypad inputs.",
            "Develop an access control system that uses an ultrasonic sensor to detect when someone approaches, activates a PIR sensor for motion detection, and only allows entry if a valid RFID card is presented? The system should display the temperature and humidity on an LCD and provide visual feedback through the RGB LED.",
            "Design a Toll Plaza system using RFID sensor, servo motor, keypad, ir sensor, 16*2 LCD Display and make sure the card is rechargeable and the deducted amount, available amount should be displayed on the LCD screen.",
            "Create a remote-controlled robotic arm using a joystick and servo motors. The Arduino should interpret the joystick inputs to control the servo motor angles, and the system should be portable, powered by a 9V battery."
        ]
        mediumQuestionsSet1 = [
            "Design a circuit to control a 6V mini water pump using an Arduino, a 5V relay module, and a 9V battery. Include an emergency cut-off mechanism using a push-button and an LED indicator to show the system's status.",
            "Design a circuit that uses a 9V battery to power both a 5V relay module and a 16x2 LCD display without causing voltage drops that could affect the system's stability. Include considerations for current consumption.",
            "Create a system that plays a recorded voice message when someone presses a button. The voice message should stop playing as soon as the button is released. How would you set this up?",
            "Create a laser-based intruder detection system where an interrupted laser beam triggers an alarm, displays a warning message on an LCD, and turns on an LED. The display should have adjustable brightness using a potentiometer.",
            "Design a system that automatically waters plants when soil moisture is low, provides feedback on environmental stability using the accelerometer, and triggers an alarm if the system is moved or tilted unexpectedly? The current status of the system should be displayed on an LCD, with an LED indicating active watering."
        ]
        mediumQuestionsSet2 = [
            "Create an environmental data logger that records temperature, humidity, and air quality data over time? The system should display real-time data on an LCD and sound an alarm if any reading exceeds predefined thresholds.",
            "Develop a gesture-based lighting control system where the joystick is used to adjust the colour and intensity of an RGB LED strip? The system should provide smooth control over the lighting environment based on the position and movement of the joystick.",
            "Design an air quality monitoring system that not only measures air quality using the MQ-135 sensor but also automatically opens a window (using the servo motor) and turns on an air purifier (via the relay) when poor air quality is detected. The RGB LED should change colour based on air quality levels.",
            "Build an anti-theft system for a portable device. Use the ADXL335 accelerometer to detect movement beyond a certain threshold, and when triggered, the Arduino should activate a relay that cuts off power to a critical component (simulating an alarm or disabling the device). Ensure the system operates on battery power for mobility.",
            "Develop a voice-controlled system that allows users to record and play back messages with directional control. Use the joystick to navigate between different recorded messages stored on the ISD1820, and play back the selected one via the speaker."
        ]
        questions = [
            hardQuestions[random.randint(0, 4)],
            mediumQuestionsSet1[random.randint(0, 4)],
            mediumQuestionsSet2[random.randint(0, 4)],
        ]
        body = {"values": [[id, teamName, questions[0], questions[1], questions[2]]]}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SHEET_ID,
                range="Round2",
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        return questions
