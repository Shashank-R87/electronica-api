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
            "question": "Which component is commonly used in an RGB cathode diffuser to achieve uniform light diffusion?",
            "options": [
                "High-gloss metal",
                "Transparent acrylic or polycarbonate",
                "Opaque plastic",
                "Reflective foil",
            ],
        },
        {
            "id": 12,
            "question": "What is the primary function of a servo motor?",
            "options": [
                "To provide continuous rotation at variable speeds",
                "To perform precise control of angular position",
                "To convert electrical energy into heat",
                "To store electrical energy",
            ],
        },
        {
            "id": 13,
            "question": "Which component in a servo motor is responsible for providing feedback on the position of the motor shaft?",
            "options": ["Gearbox", "Potentiometer", "Power supply", "Heat sink"],
        },
        {
            "id": 14,
            "question": "What is the purpose of the pinMode() function when using an LED with Arduino?",
            "options": [
                "To set the pin as either input or output",
                "To set the brightness of the LED",
                "To read the state of the pin",
                "To change the color of the LED",
            ],
        },
        {
            "id": 15,
            "question": "Arduino IDE consists of 2 functions. What are they?",
            "options": [
                "Loop() and build() and setup()",
                "Build() and loop()",
                "Setup() and build()",
                "Setup() and loop()",
            ],
        },
        {
            "id": 16,
            "question": "What is the primary purpose of a servo motor in a control system?",
            "options": [
                "To maintain a constant speed",
                "To provide precise position control",
                "To convert AC to DC",
                "To generate high torque",
            ],
        },
        {
            "id": 17,
            "question": "What is the primary function of a relay module in an electronic circuit?",
            "options": [
                "To amplify signals",
                "To switch high-current loads using a low-current control signal",
                "To convert AC to DC",
                "To measure voltage and current",
            ],
        },
        {
            "id": 18,
            "question": "When interfacing a relay module with an Arduino, which pin on the relay module is used to control the relay?",
            "options": ["VCC", "GND", "IN", "COM"],
        },
        {
            "id": 19,
            "question": "When interfacing a 4x4 keyboard matrix with a microcontroller, how many I/O pins are typically required?",
            "options": ["4", "8", "12", "16"],
        },
        {
            "id": 20,
            "question": "In a home automation project aimed at controlling lighting based on ambient light levels, which combination of components would be most appropriate?",
            "options": [
                "Light Sensor, Relay Module, 5V Power Supply",
                "Motion Detector, RGB LED Strip, Arduino Board",
                "Temperature Sensor, Servo Motor, Power Adapter",
                "Humidity Sensor, DC Motor, Resistor Array",
            ],
        },
        {
            "id": 21,
            "question": "In a project where you need to interact with users through a physical interface, which set of components would be most relevant?",
            "options": [
                "LEDs, Resistors, and Capacitors",
                "Push buttons, Potentiometers, and LCD displays",
                "Diodes, Transistors, and Inductors",
                "Relays, Transformers, and Motors",
            ],
        },
        {
            "id": 22,
            "question": "Which combination of components would be the most effective for creating a temperature-controlled fan system where the fan activates when the temperature exceeds a set threshold?",
            "options": [
                "Temperature Sensor, 5V Relay Module, DC Fan",
                "Humidity Sensor, PWM Controller, DC Fan",
                "Light Sensor, 12V Relay Module, AC Fan",
                "Pressure Sensor, 5V Transistor, DC Motor",
            ],
        },
        {
            "id": 23,
            "question": "If you need to create a system that triggers an alarm when a certain condition is met, which combination of components would be most appropriate?",
            "options": [
                "Arduino UNO, Buzzer, ADXL335 Accelerometer",
                "Push Button, 5V Relay Module, LED",
                "LDR Light Sensor, 9V Battery, 4 x 4 Keypad Matrix",
                "Moisture Sensor, 5V Relay Module, Buzzer",
            ],
        },
        {
            "id": 24,
            "question": "You need to build an interactive installation that changes colors based on the movement of a joystick. What is the most appropriate set of components?",
            "options": [
                "Joystick, RGB LED Strip, Resistor Box",
                "Joystick, RGB LED Strip, Capacitor Box",
                "Joystick, RGB Diffused Common Cathode, Resistor Box",
                "Joystick, RGB Diffused Common Cathode, Capacitor Box",
            ],
        },
        {
            "id": 25,
            "question": "The contrast of the 16 x 2 LCD display is typically adjusted using a __________.",
            "options": [
                "300 ohms Resistor",
                "10k ohm Potentiometer",
                "9V battery",
                "Push button",
            ],
        },
        {
            "id": 26,
            "question": "The component used to emit a narrow, focused beam of light in optical communication systems is the __________.",
            "options": [
                "Infrared LED",
                "KY 008 Laser Emitter",
                "Photodiode",
                "Fiber Optic Transmitter",
            ],
        },
        {
            "id": 27,
            "question": "A project requires the creation of a security system that can detect human motion in the dark and alert the user through a sound. Which components will you choose?",
            "options": [
                "Ultrasonic Sensor, SG90 Servo Motor, RGB LED Strip",
                "PIR Sensor, Piezo Buzzer, Arduino Cable",
                "IR Sensor, Electric Microphone, DHT11 Sensor",
                "Joystick, Speaker with ISD1820, Capacitor Box",
            ],
        },
        {
            "id": 28,
            "question": "In an automatic lighting system, the __________ can be used to detect when it gets dark, triggering the lights to turn on.",
            "options": [
                "Phototransistor",
                "LDR Light Sensor",
                "Infrared Proximity Sensor",
                "Photodiode",
            ],
        },
        {
            "id": 29,
            "question": "The Arduino board is also called a _______?",
            "options": ["Microprocessor", "Timer", "Oscillator", "Microcontroller"],
        },
        {
            "id": 30,
            "question": "_____ is the language used by the Arduino IDE.",
            "options": ["C", "C++", "Java", "Python"],
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
        "11": "2",
        "12": "2",
        "13": "2",
        "14": "1",
        "15": "4",
        "16": "2",
        "17": "2",
        "18": "3",
        "19": "2",
        "20": "1",
        "21": "2",
        "22": "1",
        "23": "1",
        "24": "1",
        "25": "2",
        "26": "2",
        "27": "2",
        "28": "2",
        "29": "4",
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


@app.get("/getround2/")
def getRound2():
    questionPresent = False

    if not questionPresent:
        hardQuestions = [
            "Design a temperature-controlled cooling system using an Arduino, a DHT11 temperature and humidity sensor, a 5V relay module, a 12V DC fan, and a 12V power supply. Include an LCD display to show the current temperature and humidity. The fan should turn on when the temperature exceeds a set threshold (e.g., 30°C) and turn off when the temperature drops below this threshold. Additionally, incorporate an emergency shutoff mechanism using a push-button, and an LED to indicate whether the system is active or in emergency mode.",
            "Create a system where a laser-based security alarm is activated when the laser beam is interrupted, and the alarm can only be turned off by entering a code on the keypad? The system should also control an external device via the relay, triggered by specific keypad inputs.",
            "Develop an access control system that uses an ultrasonic sensor to detect when someone approaches, activates a PIR sensor for motion detection, and only allows entry if a valid RFID card is presented? The system should display the temperature and humidity on an LCD and provide visual feedback through the RGB LED.",
            "Design a Toll Plaza system using RFID sensor, servo motor, keypad, ir sensor, 16*2 LCD Display and make sure the card is rechargeable and the deducted amount, available amount should be displayed on the LCD screen.",
            "Create a remote-controlled robotic arm using a joystick and servo motors. The Arduino should interpret the joystick inputs to control the servo motor angles, and the system should be portable, powered by a 9V battery.",
        ]
        mediumQuestionsSet1 = [
            "Design a circuit to control a 6V mini water pump using an Arduino, a 5V relay module, and a 9V battery. Include an emergency cut-off mechanism using a push-button and an LED indicator to show the system's status.",
            "Design a circuit that uses a 9V battery to power both a 5V relay module and a 16x2 LCD display without causing voltage drops that could affect the system's stability. Include considerations for current consumption.",
            "Create a system that plays a recorded voice message when someone presses a button. The voice message should stop playing as soon as the button is released. How would you set this up?",
            "Create a laser-based intruder detection system where an interrupted laser beam triggers an alarm, displays a warning message on an LCD, and turns on an LED. The display should have adjustable brightness using a potentiometer.",
            "Design a system that automatically waters plants when soil moisture is low, provides feedback on environmental stability using the accelerometer, and triggers an alarm if the system is moved or tilted unexpectedly? The current status of the system should be displayed on an LCD, with an LED indicating active watering.",
        ]
        mediumQuestionsSet2 = [
            "Create an environmental data logger that records temperature, humidity, and air quality data over time? The system should display real-time data on an LCD and sound an alarm if any reading exceeds predefined thresholds.",
            "Develop a gesture-based lighting control system where the joystick is used to adjust the colour and intensity of an RGB LED strip? The system should provide smooth control over the lighting environment based on the position and movement of the joystick.",
            "Design an air quality monitoring system that not only measures air quality using the MQ-135 sensor but also automatically opens a window (using the servo motor) and turns on an air purifier (via the relay) when poor air quality is detected. The RGB LED should change colour based on air quality levels.",
            "Build an anti-theft system for a portable device. Use the ADXL335 accelerometer to detect movement beyond a certain threshold, and when triggered, the Arduino should activate a relay that cuts off power to a critical component (simulating an alarm or disabling the device). Ensure the system operates on battery power for mobility.",
            "Develop a voice-controlled system that allows users to record and play back messages with directional control. Use the joystick to navigate between different recorded messages stored on the ISD1820, and play back the selected one via the speaker.",
        ]
        questions = [
            hardQuestions[random.randint(0, 4)],
            mediumQuestionsSet1[random.randint(0, 4)],
            mediumQuestionsSet2[random.randint(0, 4)],
        ]

        return questions
