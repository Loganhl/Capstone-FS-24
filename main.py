from keystroker import on_press, on_release
from pynput import keyboard
from pynput import mouse
import threading

# ================================
# SECTION 1: 2FA OTP Generation and Verification
# ================================

##from TwoFactor.send_email import send_email
#import pyotp

#def two_factor_auth():
  #  """Handles the OTP generation, sending, and verification."""
    
    # Generate a new secret dynamically
   # secret = pyotp.random_base32()
    
    # Create a TOTP instance with a custom interval of 10 minutes (600 seconds)
   # totp = pyotp.TOTP(secret, interval=600)
    
    # Generate an OTP using the TOTP instance
   # otp = totp.now()  # Generates a time-based OTP

    # Send OTP to user's email
  #  user_email = input("Enter your email address: ")  # Ask for the user's email
  #  send_email(user_email, otp)  # Call the function from send_email.py

    # Ask user to input OTP
  #  user_input = input("Enter the OTP sent to your email: ")

    # Verify the OTP
  #  if totp.verify(user_input):
   #     print("OTP verified successfully.")
   # else:
   ##     print("Invalid OTP or OTP has expired.")

# ================================
# SECTION 2: Keystroke Listener
# ================================
def start_keystroke_listener():
    """Starts the keyboard listener."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 

# ================================
# SECTION 3: Mouse Listener
# ================================
# Function to handle mouse movements
def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

# Function for mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        print(f"Mouse Released at ({x}, {y}) with {button}")

# Function for mouse scrolls
def on_scroll (x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with scroll ({dx}, {dy})")

# Set up the listener for mouse events
def start_mouse_listener():
    """Starts the mouse listener."""
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

# ================================
# MAIN FUNCTION
# ================================
def main():
    """Main entry point for the application."""
    
    # Call the 2FA section
    #two_factor_auth()

 # Create separate threads for the keyboard and mouse listeners
    keyboard_thread = threading.Thread(target=start_keystroke_listener)
    mouse_thread = threading.Thread(target=start_mouse_listener)

    # Start both threads
    keyboard_thread.start()
    mouse_thread.start()

    # Wait for both threads to complete (join)
    keyboard_thread.join()
    mouse_thread.join()

if __name__ == "__main__":
    main()
