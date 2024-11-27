import tkinter as tk
from tkinter import simpledialog

class CredentialsDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)

        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        return self.username_entry  # initial focus

    def apply(self):
        self.result = (self.username_entry.get(), self.password_entry.get())

def prompt_for_credentials():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    dialog = CredentialsDialog(root)
    return dialog.result



# def prompt_for_credentials():
#     # Create the root window
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window

#     # Prompt for username
#     username = simpledialog.askstring("Username", "Enter your username:")
#     if username is None:  # User clicked cancel
#         return None, None

#     # Prompt for password
#     password = simpledialog.askstring("Password", "Enter your password:", show='*')
#     if password is None:  # User clicked cancel
#         return None, None

#     return username, password

# Get credentials from user
# user, pwd = prompt_for_credentials()
