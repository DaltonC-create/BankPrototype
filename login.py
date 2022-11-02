"""
This class creates the window for the login page that also has functionality for resetting a password.
"""
import tkinter as tk
import summary
from tkinter import messagebox
from tkinter.simpledialog import askstring


class LoginPage:

    # Constructor
    def __init__(self, root, users):
        self.root = root
        self.root.title("Login")
        self.username = None
        self.password = None
        # List for user objects.
        self.users = users

        # Variable to hold user's account object.
        self.user = None

        # Canvas widget for the logo.
        self.canvas = tk.Canvas(self.root, width=350, height=130)
        # Set up logo image.
        self.logo_img = tk.PhotoImage(file="silicon-wraiths-logo.png")

        # Username widgets.
        self.username_frame = tk.Frame(self.root)
        self.username_label = tk.Label(self.username_frame, text="Username:")
        self.username_entry = tk.Entry(self.username_frame, width=37)

        # Password widgets.
        self.password_frame = tk.Frame(self.root)
        self.password_label = tk.Label(self.password_frame, text="Password:")
        self.password_entry = tk.Entry(self.password_frame, width=37, show="*")

        # Button widgets for sign in and password reset.
        self.buttons_frame = tk.Frame(self.root, pady=10)
        self.sign_in_button = tk.Button(self.buttons_frame, width=15, text="Sign-in", command=self.verify_login)
        self.reset_button = tk.Button(self.buttons_frame, width=15, text="Forgot Password", command=self.reset_password)

        self.setup_login_page()

    # Sets up locations of widgets for login page window.
    def setup_login_page(self):
        # Canvas for group logo.
        self.canvas.create_image(178, 50, image=self.logo_img)
        self.canvas.pack(anchor=tk.CENTER, pady=20)

        # Username row.
        self.username_frame.pack(anchor=tk.CENTER)
        self.username_label.grid(column=0, row=0, sticky="w")
        self.username_entry.grid(column=0, row=1)
        # Makes insertion point start on username when opening application.
        self.username_entry.focus()

        # Password row.
        self.password_frame.pack(anchor=tk.CENTER, pady=5)
        self.password_label.grid(column=0, row=0, sticky="w")
        self.password_entry.grid(column=0, row=1)

        # Buttons row.
        self.buttons_frame.pack(anchor=tk.CENTER)
        self.sign_in_button.grid(column=0, row=0, padx=5)
        self.reset_button.grid(column=1, row=0, padx=5)

    # Verify the login information.
    def verify_login(self):
        if self.login_correct():
            summary.SummaryPage(self.user)
            self.root.withdraw()
        else:
            messagebox.showwarning(title="Incorrect", message="Username or Password is incorrect.")
            self.root.focus()

    # Returns true if the username and password are correct.
    def login_correct(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        # Check the username and passwords with those available.
        for i in self.users:
            if self.username == i.username and self.password == i.password:
                self.user = i
                return True
        return False

    # Function to reset an account's password.
    def reset_password(self):
        correct_username = False
        name_user = askstring("Reset Password", "Enter Username:")
        for i in self.users:
            if name_user == i.username:
                correct_username = True
                break
        # Must not be empty or an invalid username.
        if name_user == "" or not correct_username:
            messagebox.showwarning(title="Invalid Username", message="Username not valid. Please try again.")
        else:
            messagebox.showinfo("E-mail Sent", f"A password reset link was sent to the email associated with: "
                                               f"{name_user}")
