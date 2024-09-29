from keystroker import on_press,on_release
from pynput import *




def main():
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
main()


# Import 2FA branch
from TwoFactor.generate_otp import generate_otp
from TwoFactor.send_email import send_email
from TwoFactor.verify_otp import verify_otp
# Generate an OTP
otp = generate_otp()

# Send OTP to user's Email
user_email = "user@example.com"
send_email(user_email, otp)

# Ask user to input OTP
user_input = input("Enter the OTP sent to your email: ")

# Verify the OTP
if verify_otp(user_input, otp):
    print("OTP verified successfully")
else:
    print("Invalid OTP")