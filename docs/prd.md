# CareBridge: Product Requirements Document (PRD)

## 1. Problem

Elderly people living alone often don't have someone checking in on them daily. Their kids or family may live far away and can't always tell if something is wrong like missed medication, unusual silence, a change in mood, or a broken routine. By the time family finds out, it's often too late.

## 2. Vision

CareBridge is a voice-based companion app that checks in on elderly people every day, listens for changes in how they speak or behave, and alerts their family when something feels off, before it becomes a bigger problem.

## 3. Target Users

### Primary User — The Elderly Person
- Lives alone
- Has family who live far away or can't check in daily
- Comfortable with a phone call (doesn't need to use an app or smartphone)
- Wants to feel like someone is looking out for them, without feeling watched or controlled

### Secondary User — The Family Member
- Lives far from their elderly parent/relative
- Worried about their loved one but can't call every day
- Wants peace of mind, not constant anxiety
- Needs simple, clear alerts, not overwhelming data

## 4. Goals (for this 10-day build)

- Build a working prototype that can:
  1. Call an elderly user daily
  2. Understand what they say
  3. Detect if something seems "off"
  4. Alert a family member if needed
- Test it with real people, not just fake data
- Keep it simple enough to explain in a demo

## 5. Core Features 

### Feature 1: Daily Voice Check-In
- App calls the user once a day at a set time
- Asks simple questions (e.g., "How are you feeling today?", "Did you take your medicine?")
- Records their response

### Feature 2: Speech-to-Text
- Converts the recorded voice response into text
- So we can analyze what was actually said

### Feature 3: AI Analysis
- Looks at the text and checks for:
  - Signs of confusion or distress
  - Missed routine (e.g., didn't take medicine)
  - Unusual tone or behavior compared to past check-ins
- Decides: is this normal, or does family need to know?

### Feature 4: Family Alerts
- If something seems off, send an SMS or email to the family member
- Message should be short, clear, and not alarming unless truly needed

### Feature 5: Simple Family Dashboard
- A basic web page where family can see:
  - Check-in history (did the call happen?)
  - Past alerts
  - A simple status (all good / needs attention)

## 6. Out of Scope

- Mobile app (we're using phone calls now, but maybe it will be an app the user installs in near future)
- Multiple languages
- Complex health tracking (heart rate, sleep, etc.)
- Payment/subscription system

## 7. Success Looks Like

- Real people who will test get at least one working check-in call
- The system correctly flags at least one real "something feels off" moment
- Family members say the alert felt useful, not annoying
- We have a working demo we can show and explain clearly

## 8. Tech Stack (Reference)

- **Backend:** Python + FastAPI
- **Voice Calls:** Twilio
- **Speech-to-Text:** OpenAI Whisper API
- **AI Analysis:** OpenAI GPT API
- **Database:** Firebase / SQLite
- **Alerts:** Twilio SMS / SendGrid Email
- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** Render (backend), Netlify (frontend)