import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import pyotp
import time

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
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def two_factor_auth():
    """Handles the OTP generation, sending, and verification."""
    
    # Generate and use a fixed secret for both generation and verification
    secret = pyotp.random_base32()  # Generate a valid Base32 secret
    totp = pyotp.TOTP(secret)  # Create a TOTP instance with the secret

    # Log the current system time for debugging
    print(f"Current system time (seconds since epoch): {int(time.time())}")

    # Generate an OTP using the TOTP instance
    otp = totp.now()  # Generates a time-based OTP

    # Send OTP to user's email
    user_email = input("Enter your email address: ")  # Ask for the user's email
    send_email(user_email, otp)

    # Ask user to input OTP
    user_input = input("Enter the OTP sent to your email: ")

    # Log the system time again for verification debugging
    print(f"System time when verifying (seconds since epoch): {int(time.time())}")

    # Verify the OTP using the same TOTP instance and secret with a valid window
    if totp.verify(user_input, valid_window=1):  # Allows a small window for time drift
        print("OTP verified successfully")
    else:
        print("Invalid OTP or OTP has expired")

# Main function
def main():
    """Main entry point for the application."""
    
    # Call the 2FA section
    two_factor_auth()

if __name__ == "__main__":
    main()
