<div align="center">
	<h1>Conversational IVR Modernization Framework</h1>
	<h2>Topic: In-Patient Service Request &amp; Facility Dispatch IVR</h2>
</div>

<p align="center">
	<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" />
	<img src="https://img.shields.io/badge/Twilio-ff3366?style=for-the-badge&logo=twilio" alt="Twilio" />
	<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python" alt="Python" />
	<img src="https://img.shields.io/badge/NGROK-000000?style=for-the-badge" alt="ngrok" />
</p>

> A lightweight, voice-first framework to modernize in-patient service requests and facility dispatch using conversational IVR patterns.

---

## Overview

This repository contains a prototype Conversational IVR framework that accepts inbound voice calls, interprets natural language or DTMF input, confirms intent with the caller, and routes requests to downstream teams (housekeeping, maintenance, nursing, IT). It is intended for research, prototyping, and early-stage integrations with hospital workflows.

Key goals:
- Reduce friction for patients who need services from their bedside
- Provide reliable fallbacks (DTMF) and confirmations to avoid incorrect dispatches
- Demonstrate an extensible architecture that can scale from prototype to production

## Core Innovation

- Speech-first intent resolution with DTMF fallback for robustness
- Multi-turn confirmation flows to reduce false positives and misrouted requests
- Pluggable handlers for different facility teams enabling easy extension
- Session-aware conversations for context (in-memory by default; swap to Redis for scale)

## Architecture

High-level architecture:

```
Caller (Phone)
	└─> Twilio (Voice Webhook)
				 └─> FastAPI /voice endpoint
							 ├─ Speech/DTMF -> intent resolver
							 ├─ Session store (in-memory | Redis)
							 └─ Handlers -> Dispatch (HTTP/Queue/SMS)
```

- Twilio: handles telephony, speech-to-text, and TwiML responses
- FastAPI: receives webhooks, resolves intents, and returns TwiML
- Session store: holds short-lived conversation state
- Dispatch layer: integration points to notify teams (HTTP callbacks, message queue, SMS)

## Technical Workflow

1. Twilio receives the call and POSTs to `/voice` webhook.
2. The `/voice` handler responds with a prompt asking for the request.
3. Caller replies (speech) or presses DTMF.
4. Twilio returns the speech result (or DTMF digits) to `/handle-intent`.
5. Intent resolver extracts target service, urgency, and optional metadata (room number, etc.).
6. The IVR confirms the interpreted request with the caller.
7. On confirmation, the system logs the request and triggers a dispatch action (HTTP POST to an endpoint, enqueue job, or send SMS).

## Project Structure

Root layout (key files):

- `backend_main.py` — FastAPI app with `/voice`, `/handle-intent`, and handler endpoints
- `trigger_call.py` — helper to place a test call via Twilio API
- `test_ivr.py` — unit/integration tests for core endpoints
- `audio_cache/` — generated or cached audio used during testing
- `README.md` — this file

Add or replace components:
- `sessions/` — (optional) Redis-backed session manager
- `handlers/` — pluggable handler modules (housekeeping, maintenance, nursing, IT)

## API Reference

Endpoints (summary):

- `POST /voice` — Twilio webhook for incoming calls. Returns TwiML to prompt caller.
- `POST /handle-intent` — Receives speech/DTMF results, resolves intent, and returns TwiML confirmation prompts.
- `POST /dispatch` — Internal endpoint that triggers downstream notifications (used by handlers).

Request/Response notes:
- All Twilio webhooks are POST and expect form-encoded fields from Twilio (SpeechResult, Digits, CallSid, From, etc.).
- Responses are TwiML XML. Helper methods in `backend_main.py` build TwiML for prompts and hangups.

---

**Why this exists:** voice-first prototypes are fun to build and brutally revealing for UX. This repo helps you explore voice interactions, confirm assumptions quickly, and ship a working prototype.

**Stack:** `FastAPI`, `Twilio` (voice), simple in-memory sessions (swap to Redis), and a tiny test harness (`trigger_call.py`).

**Vibe:** Playful, pragmatic, and prototype-friendly.

---

**What's inside**
- `backend_main.py` — FastAPI app and webhook handlers
- `trigger_call.py` — simulated call driver for local testing
- `test_ivr.py` — lightweight tests for core flows
- `audio_cache/` — transient audio assets used during development

**Core ideas**
- Natural language with DTMF fallback
- Multi-turn confirmations to reduce errors
- Pluggable TTS/voice providers for personality experiments

---

**Quick Start — 2-minute demo**
1. Create a virtual env and install essentials:

```bash
python -m venv .venv
.venv\\Scripts\\activate   # Windows
pip install fastapi uvicorn twilio python-dotenv pytest
```

2. Add a `.env` with your Twilio creds (or set env vars):

```
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_PHONE_NUMBER=+1##########
NGROK_URL=https://your-ngrok.ngrok.io
```

3. Run the app and expose the port:

```bash
uvicorn backend_main:app --host 0.0.0.0 --port 8000 --reload
# (optional) ngrok http 8000
```

4. Point Twilio voice webhook to `https://<your-ngrok>/voice` or run a simulated call:

```bash
python trigger_call.py
```

---

**Playground Walkthrough (human transcript)**

IVR: "Hi — this is the hospital concierge. What can I do for you today?"
Caller: "Clean my room and bring new towels, room 402." 
IVR: "Housekeeping for room 402 — confirm?"
Caller: "Yes."
IVR: "Done. We'll notify housekeeping now. Anything else?"

---

**Developer notes**
- Intent resolver is intentionally tiny — add verbs and route them to specific handlers.
- Sessions are in-memory for speed; switch to Redis when you want persistence across workers.
- Replace the built-in TTS with Amazon Polly/Google for different voices.

**Run tests**

```bash
pytest test_ivr.py
```

---

**Creative next steps**
- Give the IVR a persona (cheerful, clinical, empathetic) by swapping TTS voices and scripts.
- Add a short GIF of a test call and drop it in the repo root for a visual demo.
- Add CI that runs `pytest` on PRs and posts results to the repo.

---

