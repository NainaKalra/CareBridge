from fastapi import FastAPI
from fastapi.responses import Response
from twilio.rest import Client
from dotenv import load_dotenv
from fastapi import FastAPI, Form
import os

load_dotenv()

app = FastAPI()

# Twilio credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.get("/")
def read_root():
    return {"message": "CareBridge backend is running!"}


@app.post("/trigger-call")
def trigger_call(to_number: str):
    """
    Triggers a call to the given phone number.
    Twilio will fetch instructions from /voice-response
    """
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        url="https://awry-until-unpaid.ngrok-free.dev/voice-response" #ngrok 
    )
    return {"call_sid": call.sid, "status": "Call triggered"}


@app.post("/voice-response")
def voice_response():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather input="speech" action="https://awry-until-unpaid.ngrok-free.dev/process-speech" method="POST" speechTimeout="auto">
            <Say voice="Polly.Joanna">Hi! This is your daily check in from Care Bridge. How are you feeling today?</Say>
        </Gather>
        <Say>We didn't catch that. Have a great day!</Say>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")


@app.post("/process-speech")
def process_speech(SpeechResult: str = Form(default="")):
    print(f"User said: {SpeechResult}")
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>Thank you! Have a great day.</Say>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")