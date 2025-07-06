# email_utils.py
import random
import string
from email.message import EmailMessage
import aiosmtplib
import os
from dotenv import load_dotenv


load_dotenv()

EMAIL_HOST = os.getenv("MAIL_SERVER")
EMAIL_PORT = int(os.getenv("MAIL_PORT"))
EMAIL_SENDER = os.getenv("MAIL_FROM")
EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

async def send_otp_email(to_email: str, otp_code: str):
    subject = "Your OTP Code"
    body = f"Your OTP is: {otp_code}. It will expire in 5 minutes."

    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        start_tls=True,
        username=EMAIL_SENDER,
        password=EMAIL_PASSWORD,
    )

