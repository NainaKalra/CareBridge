from fastapi import FastAPI
from fastapi.responses import Response
from twilio.rest import Client
from dotenv import load_dotenv
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
    """
    This is what Twilio calls when the phone is picked up.
    It tells Twilio what to say and to record the response.
    """
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="Polly.Joanna">Hi! This is your daily check in from Care Bridge. How are you feeling today? Please speak after the beep.</Say>
        <Record maxLength="30" playBeep="true" />
        <Say>Thank you! Have a great day.</Say>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")