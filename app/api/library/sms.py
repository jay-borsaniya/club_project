from flask import current_app as app
from twilio.rest import Client

TWILIO_SID = "ACb23db48c5085d3d5cffea8b5f2f10217"
TWILIO_AUTH_TOKEN = "4c400c3c31a764c261593f2e4556c65b"
TWILIO_MOBILE_NUMBER = "+16202622097"

def send_sms(mobile, text):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body = str(text),
        from_ = TWILIO_MOBILE_NUMBER,
        to = "+91" + mobile
    )
    return {'status': 200, 'body': "success"}
