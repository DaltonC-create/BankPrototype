"""
This class establishes the window for the summary page, and access to all other pages.
"""
import tkinter as tk
import settings
import transfer
import check
import appointment
from app import App
from tkinter import messagebox


class SummaryPage(App):

    # Constructor.
    def __init__(self, user):
        super().__init__()
        self.root = self
        self.title("Account Summary")
        self.user = user

        # Handle the user closing the window instead of using logout button.
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

        # Account name title.
        self.account_title = tk.Label(self.root, text=f"{self.user.first_name} {self.user.last_name}'s Account",
                                      font=self.text_font)

        # Main frame.
        self.main_frame = tk.Frame(self.root)
        # Add space between widgets.
        self.main_frame.columnconfigure(1, weight=1, minsize=20)
        self.main_frame.rowconfigure(1, weight=1, minsize=10)

        # Account summary widgets.
        self.accounts_frame = tk.Frame(self.root)
        self.checking_label = tk.Label(self.accounts_frame, text=f"Checking Account: ${self.user.checking:.2f}",
                                       font=self.text_font)
        self.savings_label = tk.Label(self.accounts_frame, text=f" Savings Account: ${self.user.savings:.2f}",
                                      font=self.text_font)

        # Button widgets for transfer and check requests.
        self.transfer_button = tk.Button(self.main_frame, text="Transfer Funds", width=20,
                                         command=self.transfer_money)
        self.check_button = tk.Button(self.main_frame, text="Cashier's Check", width=20, command=self.cashier_check)

        # Button widgets for scheduling an appointment and account settings.
        self.appointment_button = tk.Button(self.main_frame, text="Schedule Appointment", width=20,
                                            command=self.schedule_appointment)
        self.settings_button = tk.Button(self.main_frame, text="Account Settings", width=20, command=self.settings)

        # Button widget for logging out.
        self.logout_button = tk.Button(self.root, text="Logout", width=10, command=self.logout)

        self.setup_summary_page()

    # Sets up locations of widgets for summary page window.
    def setup_summary_page(self):
        # Account name title.
        self.account_title.pack(anchor=tk.CENTER, pady=10)

        # Checking and savings account row.
        self.accounts_frame.pack(anchor=tk.CENTER, pady=20)
        self.checking_label.pack(anchor=tk.CENTER)
        self.savings_label.pack(anchor=tk.CENTER)

        # Main frame.
        self.main_frame.pack()

        # Transfer and check buttons row.
        self.transfer_button.grid(column=0, row=0, sticky="e")
        self.check_button.grid(column=2, row=0, sticky="w")

        # Appointment and settings buttons row.
        self.appointment_button.grid(column=0, row=2, sticky="e")
        self.settings_button.grid(column=2, row=2, sticky="w")

        self.logout_button.pack(anchor=tk.CENTER, pady=15)

    # Creates the window for transferring money between accounts.
    def transfer_money(self):
        transfer.TransferPage(self.user, self)

    # Creates the window for requesting a cashier's check.
    def cashier_check(self):
        check.CashiersCheckPage(self.user, self)

    # Creates the window for scheduling an appointment.
    def schedule_appointment(self):
        appointment.ScheduleAppointmentPage(self.user, self)

    def settings(self):
        settings.SettingsPage(self.user, self)

    # Logout and exit the program.
    def logout(self):
        self.root.destroy()
        messagebox.showinfo(title="Success", message="You were successfully logged out.")
        quit()

    # Refreshes the summary page.
    def refresh(self):
        self.destroy()
        self.__init__(self.user)
