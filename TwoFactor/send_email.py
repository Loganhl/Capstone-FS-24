import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

def send_email(receiver_email, otp_code):
    """Send an OTP code to the given email address."""
    smtp_server = os.getenv('SMTP_SERVER')  # smtp.gmail.com
    smtp_port = int(os.getenv('SMTP_PORT'))  # 587
    sender_email = os.getenv('SENDER_EMAIL')  # biovaultservices@gmail.com
    password = os.getenv('EMAIL_PASSWORD')  # App-specific password

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp_code}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        # Establish connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()
