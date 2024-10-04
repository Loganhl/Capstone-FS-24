#from keystroker import on_press, on_release
#from pynput import keyboard

# ================================
# SECTION 1: 2FA OTP Generation and Verification
# ================================
from TwoFactor.generate_otp import generate_totp  # Import correct method
from TwoFactor.send_email import send_email
from TwoFactor.verify_otp import verify_totp  # Import correct method
import pyotp

def two_factor_auth():
    """Handles the OTP generation, sending, and verification."""
    
    # Generate a new secret dynamically
    secret = pyotp.random_base32()
    
    # Create a TOTP instance with a custom interval of 10 minutes (600 seconds)
    totp = pyotp.TOTP(secret, interval=600)
    
    # Generate an OTP using the TOTP instance
    otp = totp.now()  # Generates a time-based OTP

    # Send OTP to user's email
    user_email = input("Enter your email address: ")  # Ask for the user's email
    send_email(user_email, otp)  # Call the function from send_email.py

    # Ask user to input OTP
    user_input = input("Enter the OTP sent to your email: ")

    # Verify the OTP
    if totp.verify(user_input):
        print("OTP verified successfully.")
    else:
        print("Invalid OTP or OTP has expired.")

# ================================
# SECTION 2: Keystroke Listener
# ================================
#def start_keystroke_listener():
 #   """Starts the keyboard listener."""
  #  with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
   #     listener.join() 

# ================================
# MAIN FUNCTION
# ================================
def main():
    """Main entry point for the application."""
    
    # Call the 2FA section
    two_factor_auth()

    # Start the keyboard listener (if needed)
   # start_keystroke_listener()

if __name__ == "__main__":
    main()
