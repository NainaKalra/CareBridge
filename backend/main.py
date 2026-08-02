from fastapi import FastAPI
from fastapi.responses import Response
from twilio.rest import Client
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, Form
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

load_dotenv()

app = FastAPI()

# Twilio credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
FAMILY_PHONE_NUMBER = os.getenv("FAMILY_PHONE_NUMBER")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
FAMILY_EMAIL = os.getenv("FAMILY_EMAIL")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Gemini setup 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-flash-latest")


#to check if the server is working
@app.get("/")
def read_root():
    return {"message": "CareBridge backend is running!"}

# Twilio will trigger call to the person
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

#Twilio converts voice to text
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

#function to check the user's response is normal or off by AI 
def analyze_checkin(text: str) -> str:
    """
    Sends the transcript to Gemini and returns 'normal' or 'needs attention'.
    """
    if not text.strip():
        return "needs attention"  # empty response = something's off

    prompt = f"""
    You are analyzing a daily check-in response from an elderly person living alone.
    Their response was: "{text}"

    Does this response sound normal, or does it show signs of confusion, distress,
    sadness, or a missed routine (like forgetting medicine)?

    Reply with ONLY one word: "normal" or "needs attention".
    """

    try:
        response = gemini_model.generate_content(prompt)
        result = response.text.strip().lower()
        if "needs attention" in result:
            return "needs attention"
        return "normal"
    except Exception as e:
        print(f"Gemini error: {e}")
        return "needs attention"

#sends alert email to family if gemini says something is off
def send_alert(transcript: str, family_email: str):
    """
    Sends an email alert to the family member when something seems off.
    """
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=family_email,
        subject="CareBridge Alert: Check-in needs your attention",
        plain_text_content=f"Something seemed a little different today during the check-in. They said: \"{transcript}\" — worth a quick call to check in."
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Alert email sent! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Failed to send alert email: {e}")
        return False

#backend will receive text, run AI analysis, and thank the user
@app.post("/process-speech")
def process_speech(SpeechResult: str = Form(default="")):
    print(f"User said: {SpeechResult}")

    result = analyze_checkin(SpeechResult)
    print(f"AI Analysis: {result}")

    if result == "needs attention":
        send_alert(SpeechResult, FAMILY_EMAIL)

    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>Thank you! Have a great day.</Say>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")