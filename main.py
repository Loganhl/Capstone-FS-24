from keystroker import on_press, on_release
from pynput import keyboard

# ================================
# SECTION 1: 2FA OTP Generation and Verification
# ================================
from TwoFactor.generate_otp import generate_totp  # Import correct method
from TwoFactor.send_email import send_email
from TwoFactor.verify_otp import verify_totp  # Import correct method
import pyotp

def two_factor_auth():
    """Handles the OTP generation, sending, and verification."""
    
    # Secret key for generating and verifying the OTP
    secret = pyotp.random_base32()  # Make sure this is constant for OTP generation and verification

    # Generate an OTP using the secret
    otp = generate_totp(secret)  # Generates a time-based OTP using the secret

    # Send OTP to user's email
    user_email = input("Enter your email address: ")
    send_email(user_email, otp)

    # Ask user to input OTP
    user_input = input("Enter the OTP sent to your email: ")

    # Verify the OTP
    if verify_totp(secret, user_input):  # Verifies the OTP using the same secret
        print("OTP verified successfully")
    else:
        print("Invalid OTP or OTP has expired")

# ================================
# SECTION 2: Keystroke Listener
# ================================
def start_keystroke_listener():
    """Starts the keyboard listener."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 

# ================================
# MAIN FUNCTION
# ================================
def main():
    """Main entry point for the application."""
    
    # Call the 2FA section
    two_factor_auth()

    # Start the keyboard listener (if needed)
    start_keystroke_listener()

if __name__ == "__main__":
    main()
