# CareBridge : Architecture Document

## 1. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Voice Calls | Twilio (Voice API) |
| Speech-to-Text | OpenAI Whisper API |
| AI Analysis | OpenAI GPT API |
| Database | Firebase (or SQLite for local dev) |
| Alerts | Twilio SMS / SendGrid Email |
| Frontend | HTML + CSS + JavaScript |
| Backend Hosting | Render / Railway |
| Frontend Hosting | Netlify / Vercel |

## 2. App Flow (How It Works, Step by Step)

```
1. SCHEDULED TRIGGER
   Backend cron job / scheduler runs at a set time each day
        │
        ▼
2. TWILIO CALLS THE USER
   Twilio dials the elderly user's phone number
   Plays a set of simple voice questions
   ("How are you feeling today?" / "Did you take your medicine?")
        │
        ▼
3. RESPONSE RECORDED
   User's spoken answer is recorded by Twilio
   Audio file is sent to our backend
        │
        ▼
4. SPEECH-TO-TEXT
   Backend sends audio to OpenAI Whisper API
   Whisper returns the text of what the user said
        │
        ▼
5. AI ANALYSIS
   Text is sent to OpenAI GPT API along with past check-in history
   GPT checks for:
     - signs of confusion / distress
     - missed routine (e.g. medicine not taken)
     - unusual tone vs previous check-ins
   GPT returns a simple result: "normal" or "needs attention"
        │
        ▼
6. SAVE TO DATABASE
   Check-in result, transcript, and AI analysis saved to database
        │
        ▼
7. DECISION
   ┌─────────────┴─────────────┐
   │                           │
 NORMAL                  NEEDS ATTENTION
   │                           │
   ▼                           ▼
No alert sent          Alert sent to family
Just logged in DB       via SMS (Twilio) or Email (SendGrid)
                                │
                                ▼
8. FAMILY DASHBOARD
   Family logs into simple web dashboard (HTML/CSS/JS)
   Dashboard calls backend API to fetch:
     - check-in history
     - alerts
     - current status (all good / needs attention)
```

## 3. System Components

```
┌─────────────────┐
│   Twilio         │  → Makes daily calls, records responses,
│  (Voice + SMS)   │     sends alert SMS
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend │  → Core logic, connects everything together
└────────┬─────────┘
         │
   ┌─────┼──────────────┬──────────────┐
   ▼     ▼               ▼              ▼
┌──────┐ ┌───────────┐ ┌───────────┐ ┌──────────┐
│Whisper│ │ GPT API   │ │  Database │ │ SendGrid │
│(STT) │ │(Analysis) │ │(Firebase/ │ │ (Email)  │
│      │ │           │ │ SQLite)   │ │          │
└──────┘ └───────────┘ └───────────┘ └──────────┘

         ▲
         │ (fetch data via API)
         │
┌─────────────────┐
│ Family Dashboard │  → HTML/CSS/JS frontend, hosted separately
│  (Frontend)      │
└──────────────────┘
```

## 4. Folder / File Structure

```
carebridge/
│
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # API keys (Twilio, OpenAI, etc.) — not committed
│   │
│   ├── routes/
│   │   ├── call_routes.py       # Endpoints to trigger/receive calls
│   │   ├── checkin_routes.py    # Endpoints for check-in data
│   │   └── alert_routes.py      # Endpoints for sending/viewing alerts
│   │
│   ├── services/
│   │   ├── twilio_service.py    # Twilio call + SMS logic
│   │   ├── whisper_service.py   # Speech-to-text logic
│   │   ├── gpt_service.py       # AI analysis logic
│   │   └── alert_service.py     # Decides & sends alerts (SMS/Email)
│   │
│   ├── models/
│   │   ├── family.py            # Family data model
│   │   ├── user.py              # Elderly user data model
│   │   └── checkin.py           # Check-in record data model
│   │
│   ├── database/
│   │   └── db.py                # Database connection (Firebase/SQLite)
│   │
│   └── scheduler/
│       └── daily_call_job.py    # Cron job to trigger daily calls
│
├── frontend/
│   ├── index.html               # Family dashboard main page
│   ├── style.css                # Styling
│   └── script.js                # Fetches data from backend API
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── README.md
│
└── .gitignore
```

## 5. Data Model (Simple Overview)

**Family**
- family_id
- family_name
- contact_email
- contact_phone

**User (Elderly Person)**
- user_id
- name
- phone_number
- family_id (linked to Family)

**Check-in**
- checkin_id
- user_id
- date
- transcript (what they said)
- ai_result ("normal" / "needs attention")
- alert_sent (true/false)

## 6. Why This Structure

- **routes/** → handles incoming requests (API endpoints)
- **services/** → all the "doing" logic (calling Twilio, calling OpenAI, etc.) stays separate from routes, so code stays clean and easy to test
- **models/** → defines what our data looks like
- **database/** → one place to manage DB connection, easy to swap Firebase ↔ SQLite later
- **scheduler/** → handles the daily automated trigger, separate from the rest of the app
