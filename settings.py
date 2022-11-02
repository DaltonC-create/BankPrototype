"""
This class establishes the window for the settings of a user's account.
"""
import tkinter as tk
import re
from app import App
from tkinter import messagebox


class SettingsPage(App):

    # Constructor.
    def __init__(self, user, summary_page):
        super().__init__()
        self.root = self
        self.title("Settings")
        self.user = user
        self.summary_page = summary_page

        # Regex to check validity of an email.
        self.regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        # Reset password variables.
        self.new_pass1 = None
        self.new_pass2 = None

        # Labels for user's information.
        self.name_label = tk.Label(self.root, text=f"{self.user.first_name} {self.user.last_name}", font=self.text_font)
        self.email_label = tk.Label(self.root, text=f"{self.user.email}", font=self.text_font)
        self.address_label = tk.Label(self.root, text=f"{self.user.address} {self.user.city}, {self.user.state}, "
                                                      f"{int(self.user.zip_code)}", font=self.text_font)

        # Buttons frame.
        self.button_frame = tk.Frame(self.root)

        # Reset password widgets.
        self.reset_password_button = tk.Button(self.button_frame, text="Reset Password",
                                               command=self.reset_password, width=15)

        # Change email widgets.
        self.change_email_button = tk.Button(self.button_frame, text="Change E-mail",
                                             command=self.change_email, width=15)
        # Change address widgets.
        self.change_address_button = tk.Button(self.button_frame, text="Change Address",
                                               command=self.change_address, width=15)
        # Button widget for returning to the summary page.
        self.back_button = tk.Button(self.button_frame, text="Back to Summary", command=self.back_to_summary, width=15)

        # Widgets for reset password window.
        self.current_pass_entry = None
        self.new_pass_entry = None
        self.new_pass_entry2 = None
        self.reset_window = None

        # Widgets for changing email window.
        self.email_window = None
        self.new_email_entry = None
        self.current_email_entry = None

        self.setup_settings_page()

    def setup_settings_page(self):
        # User information labels.
        self.name_label.pack(anchor=tk.CENTER)
        self.email_label.pack(anchor=tk.CENTER)
        self.address_label.pack(anchor=tk.CENTER)

        # Button frame.
        self.button_frame.pack(anchor=tk.CENTER, pady=20)

        # Reset password button.
        self.reset_password_button.grid(column=0, row=0, pady=10)

        # Change email button.
        self.change_email_button.grid(column=0, row=1, pady=10)

        # Change address button.
        self.change_address_button.grid(column=0, row=2, pady=10)

        # Back to summary button.
        self.back_button.grid(column=0, row=3, pady=10)

    # Sets up the reset password window.
    def reset_password(self):
        pass_win = tk.Toplevel(self.root)
        pass_win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        pass_win.title("Reset Password")
        self.reset_window = pass_win

        # Current password widgets.
        current_pass_label = tk.Label(pass_win, text="Enter current password:")
        current_pass_label.pack(anchor=tk.CENTER, pady=10)
        self.current_pass_entry = tk.Entry(pass_win, width=15)
        self.current_pass_entry.pack(anchor=tk.CENTER)

        # New password widgets.
        new_pass_label = tk.Label(pass_win, text="Enter new password:")
        new_pass_label.pack(anchor=tk.CENTER, pady=10)
        self.new_pass_entry = tk.Entry(pass_win, width=15)
        self.new_pass_entry.pack(anchor=tk.CENTER)
        # Re-enter password widgets.
        new_pass_label2 = tk.Label(pass_win, text="Enter new password:")
        new_pass_label2.pack(anchor=tk.CENTER, pady=10)
        self.new_pass_entry2 = tk.Entry(pass_win, width=15)
        self.new_pass_entry2.pack(anchor=tk.CENTER)

        # Button widgets.
        button_frame = tk.Frame(pass_win, width=40, height=30)
        button_frame.columnconfigure(1, weight=1, minsize=10)
        button_frame.pack(anchor=tk.CENTER, pady=20)
        submit_button = tk.Button(button_frame, text="Submit", command=self.check_passwords)
        submit_button.grid(column=0, row=0)
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.pass_cancel)
        cancel_button.grid(column=2, row=0)

    # Checks the passwords for errors.
    def check_passwords(self):
        # Current password is incorrect.
        if self.current_pass_entry.get() != self.user.password:
            messagebox.showerror(title="Invalid Password", message="That is not your current password.")
        # Both new password entries do not match.
        elif self.new_pass_entry.get() != self.new_pass_entry2.get():
            messagebox.showerror(title="Invalid Password", message="Passwords do not match.")
        # An entry is blank.
        elif self.new_pass_entry.get() == "":
            messagebox.showerror(title="Invalid Password", message="Password is empty.")
        # All fields were properly entered.
        else:
            self.user.password = self.new_pass_entry.get()
            messagebox.showinfo(title="Success!", message="Your password was successfully changed.")
            # Update csv file.
            self.write_to_user(self.user)
            self.pass_cancel()

    # Cancels resetting the password, going back to the settings window.
    def pass_cancel(self):
        self.reset_window.destroy()

    # Changes email of user.
    def change_email(self):
        # Open a small window.
        email_win = tk.Toplevel(self.root)
        email_win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        email_win.title("Change E-mail")
        self.email_window = email_win

        # Current email widgets.
        current_email_label = tk.Label(email_win, text="Enter current E-mail:")
        current_email_label.pack(anchor=tk.CENTER, pady=10)
        self.current_email_entry = tk.Entry(email_win, width=15)
        self.current_email_entry.pack(anchor=tk.CENTER)

        # New email widgets.
        new_email_label = tk.Label(email_win, text="Enter new E-mail:")
        new_email_label.pack(anchor=tk.CENTER, pady=10)
        self.new_email_entry = tk.Entry(email_win, width=15)
        self.new_email_entry.pack(anchor=tk.CENTER)

        # Button widgets.
        button_frame = tk.Frame(email_win, width=40, height=30)
        button_frame.columnconfigure(1, weight=1, minsize=10)
        button_frame.pack(anchor=tk.CENTER, pady=20)
        submit_button = tk.Button(button_frame, text="Submit", command=self.check_email)
        submit_button.grid(column=0, row=0)
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.email_cancel)
        cancel_button.grid(column=2, row=0)

    # Checks if user entered a new email in the proper format.
    def check_email(self):
        current_email = self.current_email_entry.get()
        new_email = self.new_email_entry.get()
        # If user did not correctly input their current email.
        if current_email != self.user.email:
            messagebox.showerror(title="Incorrect E-mail", message="That is not your current E-mail.")
        # If user did not enter a proper email.
        elif not self.is_email_format(new_email):
            messagebox.showerror(title="Invalid E-mail", message="That is not a valid E-mail address.")
        # Update user's email.
        else:
            self.user.email = new_email
            messagebox.showinfo(title="Success!", message="Your E-mail was successfully changed.")
            # Update csv file.
            self.write_to_user(self.user)
            self.email_cancel()

    # Returns true if user's new email follows an email format.
    def is_email_format(self, email):
        if re.fullmatch(self.regex, email):
            return True
        return False

    # Cancels the change email process.
    def email_cancel(self):
        self.email_window.destroy()

    # Message for changing a user's address.
    def change_address(self):
        messagebox.showinfo(title="E-mail Sent", message=f"An E-mail was sent to {self.user.email} containing the "
                                                         f"form to change your address information. You will need "
                                                         f"to bring it to a branch in person or send via mail signed "
                                                         f"and dated.")

    # Returns to the summary page.
    def back_to_summary(self):
        # Destroys current window and refreshes summary page in case of changes.
        self.root.destroy()
        self.summary_page.refresh()
