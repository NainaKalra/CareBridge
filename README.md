# CareBridge

CareBridge is a companion app for elderly people who live alone. It checks in with them every day using voice, and it listens for changes in how they speak or in their daily routine. If something seems off, it lets their family know.

## Why I'm Building This

I met an elderly woman on a bus who was trying to remember if she took her morning medicine. She lived alone and her kids were far away. She told me the hardest part of getting older wasn't her health — it was feeling like nobody was watching out for her.

That conversation stuck with me. CareBridge is my attempt to fix that problem, starting small and real, not big and fake.

## What It Does

- Calls or talks to the user once a day (voice check-in)
- Listens for changes in speech, mood, or routine
- Notices if something is off (missed medicine, unusual silence, etc.)
- Sends an alert to family members when needed

## How It's Being Built

I'm not trying to scale this to thousands of users right away. The goal is to make it actually work for real humans before thinking about growth.

## Long-Term Goal

Eventually, I want to license CareBridge to healthcare providers and senior living communities, so more elderly people can have someone "watching out" for them, even from a distance.


## Tech Stack
Python (FastAPI) + Twilio (calls & SMS) + OpenAI Whisper (speech-to-text) + OpenAI GPT (analysis) + Firebase/SQLite (database) + HTML/CSS/JS (frontend)
