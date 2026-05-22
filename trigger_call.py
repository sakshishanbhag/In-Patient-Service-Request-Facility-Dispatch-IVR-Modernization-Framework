import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Get credentials from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
base_url = os.getenv("NGROK_URL")
user_phone = os.getenv("USER_PHONE")

# Create Twilio client
client = Client(account_sid, auth_token)

# Make the call
call = client.calls.create(
    to=user_phone,
    from_=twilio_number,
    url=f"{base_url}/voice"
)

print("Call initiated:", call.sid)