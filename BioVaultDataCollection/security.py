import tkinter as tk
from tkinter import simpledialog

def prompt_for_credentials():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt for username
    username = simpledialog.askstring("Username", "Enter your username:")
    if username is None:  # User clicked cancel
        return None, None

    # Prompt for password
    password = simpledialog.askstring("Password", "Enter your password:", show='*')
    if password is None:  # User clicked cancel
        return None, None

    return username, password

# Get credentials from user
# user, pwd = prompt_for_credentials()
