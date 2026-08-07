# CareBridge

CareBridge is a companion app for elderly people who live alone. It checks in with them every day using voice, and it listens for changes in how they speak or in their daily routine. If something seems off, it lets their family know.

🔗 **Live Demo:** https://clinquant-alfajores-0d51c4.netlify.app
🔗 **Backend API:** https://carebridge-backend-927h.onrender.com

## Why I'm Building This

I met an elderly woman on a bus who was trying to remember if she took her morning medicine. She lived alone and her kids were far away. She told me the hardest part of getting older wasn't her health — it was feeling like nobody was watching out for her.

That conversation stuck with me. CareBridge is my attempt to fix that problem, starting small and real, not big and fake.

## What It Does

- Calls the user once a day (voice check-in)
- Listens for changes in speech, mood, or routine
- Notices if something is off (missed medicine, confusion, unusual silence, etc.)
- Sends an alert to family members when needed
- Gives family a simple dashboard to see check-in history and status

## How It's Being Built

I'm not trying to scale this to thousands of users right away. The goal is to make it actually work for real humans before thinking about growth. The core flow — call, speech capture, AI analysis, alerts, and dashboard — is live and working end-to-end.

## Long-Term Goal

Eventually, I want to license CareBridge to healthcare providers and senior living communities, so more elderly people can have someone "watching out" for them, even from a distance.

## Tech Stack

Python (FastAPI) + Twilio (voice calls) + Google Gemini (speech analysis) + Firebase (database) + SendGrid (email alerts) + HTML/CSS/JS (frontend) — deployed on Render (backend) and Netlify (frontend)

## Status

Core product complete — daily voice check-in, AI analysis, family alerts, and dashboard all working end-to-end, deployed and live.

## About

Built by Naina Kalra, CS student at Indiana Tech.
