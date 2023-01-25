from flask import current_app as app
from flask_mail import Message
from ...extensions import mail

def send_email(email, text):
    msg = Message("Your Otp", recipients=[email])
    msg.body = text
    mail.send(msg)
    return {'status': 200, 'body': "success"}
