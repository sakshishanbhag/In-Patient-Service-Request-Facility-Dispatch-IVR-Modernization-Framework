import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather

load_dotenv()

app = FastAPI()

# Load ngrok URL from .env
BASE_URL = os.getenv("NGROK_URL")

# Voice configuration
IVR_VOICE = "Polly.Aditi"

# Session storage
call_sessions = {}


@app.post("/voice")
async def main_menu():

    response = VoiceResponse()

    gather = Gather(
        input="speech dtmf",
        num_digits=1,
        action=f"{BASE_URL}/handle-intent",
        method="POST",
        language="en-IN",
        speechTimeout="auto"
    )

    gather.say(
        "Welcome to the In Patient Service Request system. "
        "How can I help you today? "
        "You may say housekeeping, maintenance, I T support, or nursing station.",
        voice=IVR_VOICE
    )

    response.append(gather)
    response.redirect(f"{BASE_URL}/voice")

    return Response(content=str(response), media_type="application/xml")


@app.post("/handle-intent")
async def handle_intent(
    CallSid: str = Form(...),
    SpeechResult: str = Form(default=None),
    Digits: str = Form(default=None)
):

    response = VoiceResponse()

    text = ""
    if SpeechResult:
        text = SpeechResult.lower()

    if CallSid not in call_sessions:
        call_sessions[CallSid] = {}

    if Digits == "1" or "housekeeping" in text or "clean" in text:

        call_sessions[CallSid]["intent"] = "housekeeping"

        gather = Gather(
            input="speech dtmf",
            num_digits=1,
            action=f"{BASE_URL}/handle-housekeeping",
            method="POST",
            language="en-IN",
            speechTimeout="auto"
        )

        gather.say(
            "What housekeeping service is needed? "
            "Say cleaning, spill, or fresh linens.",
            voice=IVR_VOICE
        )

        response.append(gather)

    elif Digits == "2" or "maintenance" in text:

        response.say(
            "Maintenance request registered. "
            "A technician will arrive shortly.",
            voice=IVR_VOICE
        )
        response.hangup()

    elif Digits == "3" or "it support" in text:

        response.say(
            "I T support request registered.",
            voice=IVR_VOICE
        )
        response.hangup()

    elif Digits == "4" or "nurse" in text:

        response.say(
            "Connecting to nursing station.",
            voice=IVR_VOICE
        )
        response.hangup()

    else:

        response.say(
            "Sorry, the request was not understood.",
            voice=IVR_VOICE
        )
        response.redirect(f"{BASE_URL}/voice")

    return Response(content=str(response), media_type="application/xml")


@app.post("/handle-housekeeping")
async def handle_housekeeping(
    CallSid: str = Form(...),
    SpeechResult: str = Form(default=None),
    Digits: str = Form(default=None)
):

    response = VoiceResponse()

    text = ""
    if SpeechResult:
        text = SpeechResult.lower()

    if Digits == "1" or "clean" in text:

        response.say(
            "Routine cleaning request registered. "
            "Housekeeping staff will arrive shortly.",
            voice=IVR_VOICE
        )

    elif Digits == "2" or "spill" in text:

        response.say(
            "Urgent spill cleanup reported. "
            "An emergency janitorial team has been dispatched.",
            voice=IVR_VOICE
        )

    elif Digits == "3" or "linen" in text:

        response.say(
            "Fresh linens will be delivered shortly.",
            voice=IVR_VOICE
        )

    else:

        response.say(
            "Request not understood.",
            voice=IVR_VOICE
        )

    response.hangup()

    return Response(content=str(response), media_type="application/xml")