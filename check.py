"""
This class establishes the window for requesting a cashier's check.
NOTE: Will need to import tkcalendar module to run.
"""
import tkcalendar as cal
import tkinter as tk
import datetime as dt
from tkinter import ttk, messagebox
from app import App


class CashiersCheckPage(App):

    # Constructor.
    def __init__(self, user, summary_page):
        super().__init__()
        self.root = self
        self.title("Cashier's Check")
        self.height = 600
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.user = user
        # Reference to summary page for refresh method.
        self.summary_page = summary_page

        # Options for combobox.
        self.transport_methods = ["Delivery", "Pickup"]
        # Options for accounts.
        self.account_types = ["Checking", "Savings"]

        # Variables for class methods.
        self.check_amount = None
        self.account_used = None
        self.delivery_type = None

        # Get tomorrow's date for start of date options.
        self.tomorrow = dt.datetime.today() + dt.timedelta(days=1)
        # Date variables for calendar.
        self.year = self.tomorrow.year
        self.month = self.tomorrow.month
        self.day = self.tomorrow.day
        # Previous day selected for calendar widget when error occurs.
        self.day_before_selection = self.tomorrow

        # Interactive calendar.
        self.calendar = cal.Calendar(self.root, year=self.year, month=self.month, day=self.day,
                                     mindate=self.tomorrow, showweeknumbers=False, font=self.text_font,
                                     firstweekday="sunday", showothermonthdays=False)

        # Hours label at the top of the page.
        self.hours_label = tk.Label(self.root, text="Regular Business Hours:\n9:00-5:00 Monday-Friday",
                                    font=self.text_font)

        # Main frame.
        self.main_frame = tk.Frame(self.root)
        # Add space between widgets.
        self.main_frame.columnconfigure(1, weight=1, minsize=20)

        # Dollar amount widgets.
        self.amount_label = tk.Label(self.main_frame, text="Amount:")
        self.amount_entry = tk.Entry(self.main_frame, width=16)

        # Account selection widgets.
        self.account_label = tk.Label(self.main_frame, text="Account:")
        self.account_combobox = ttk.Combobox(self.main_frame, values=self.account_types,
                                             state="readonly", width=13)

        # Delivery method widgets.
        self.method_label = tk.Label(self.main_frame, text="Delivery Method:")
        self.delivery_method = ttk.Combobox(self.main_frame, values=self.transport_methods,
                                            state="readonly", width=13)

        # Button widgets for submitting and returning to the summary page.
        self.button_frame = tk.Frame(self.root)
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_request)
        self.back_button = tk.Button(self.button_frame, text="Back to Summary", command=self.back_to_summary)

        self.setup_check_page()

    # Sets up locations of widgets for cashier's check page window.
    def setup_check_page(self):
        # Hours of Operation.
        self.hours_label.pack(anchor=tk.CENTER, pady=10)

        # Calendar.
        self.calendar.pack(anchor=tk.CENTER, pady=10)

        # Calendar binding on day selection.
        self.calendar.bind("<<CalendarSelected>>", self.verify_day_selection)

        # Main frame.
        self.main_frame.pack(anchor=tk.CENTER)

        # Dollar amount row.
        self.amount_label.grid(column=0, row=0, sticky="e")
        self.amount_entry.grid(column=2, row=0, sticky="w")

        # Account selection row.
        self.account_label.grid(column=0, row=1, sticky="e", pady=10)
        self.account_combobox.grid(column=2, row=1, sticky="w", pady=10)
        # Set default value for account to pull funds.
        self.account_combobox.current(0)

        # Delivery method row.
        self.method_label.grid(column=0, row=2, sticky="e")
        self.delivery_method.grid(column=2, row=2, sticky="w")
        # Set default value for delivery method.
        self.delivery_method.current(0)

        # Submit and back buttons row.
        self.button_frame.pack(anchor=tk.CENTER, pady=20)
        self.submit_button.grid(column=0, row=0, padx=5)
        self.back_button.grid(column=1, row=0, padx=5)

    # Returns to the summary page.
    def back_to_summary(self):
        # Destroys current window and refreshes summary page in case of changes.
        self.root.destroy()
        self.summary_page.refresh()

    # Checks if user selects a weekend day, parameter e is the event listener.
    def verify_day_selection(self, e):
        # Get selected day on calendar.
        current_selection = dt.datetime.strptime(self.calendar.get_date(), "%m/%d/%y")
        # Check if selected day is a Saturday.
        if current_selection.weekday() == 5:
            # Keep selection without changing & display error message.
            self.calendar.selection_set(self.day_before_selection)
            messagebox.showerror(title="Invalid day", message="Please only select a business day.")
        # Check if selected day is a Sunday.
        elif current_selection.weekday() == 6:
            # Keep selection without changing & display error message.
            self.calendar.selection_set(self.day_before_selection)
            messagebox.showerror(title="Invalid day", message="Please only select a business day.")
        # Selection was weekday, store date to save if a weekend day is selected next.
        else:
            self.day_before_selection = current_selection

    # Returns true if amount entered is a number and account has the funds available.
    def verify_amount(self):
        self.account_used = self.account_combobox.get()
        self.check_amount = self.amount_entry.get()
        # Check if pulling funds from checking account.
        if self.account_used == self.account_types[0] and float(self.check_amount) <= float(self.user.checking):
            self.user.checking -= float(self.check_amount)

        # Check if pulling funds from savings account.
        elif self.account_used == self.account_types[1] and float(self.check_amount) <= float(self.user.savings):
            self.user.savings -= float(self.check_amount)

        # Incorrect funds amount to pull from account.
        else:
            return False
        # Funds were successfully pulled from the account.
        return True

    # Submits the check request.
    def submit_request(self):
        # Error message if the amount is not a valid number.
        if not self.is_float(self.amount_entry.get()):
            messagebox.showerror(title="Invalid Amount", message="The check amount was not a valid number.")
            self.focus()
        # Error message if teh amount is too high for the specified account.
        elif not self.verify_amount():
            messagebox.showerror(title="Invalid Amount",
                                 message=f"The {self.account_used} account does not have enough funds.")
            self.focus()
        # Request is good and can continue.
        else:
            self.delivery_type = self.delivery_method.get()
            date = self.calendar.get_date()
            # If user selected delivery.
            if self.delivery_type == self.transport_methods[0]:
                messagebox.showinfo(title="Success!",
                                    message=f"A cashier's check in the amount of ${self.check_amount} "
                                            f"will be delivered to the address {self.user.address}, "
                                            f"{self.user.city}, {self.user.state}, "
                                            f"{self.user.zip_code} on the following date: {date}. "
                                            f"More details were sent to the following address: {self.user.email}")
            # If the user selected pickup.
            if self.delivery_type == self.transport_methods[1]:
                messagebox.showinfo(title="Success!",
                                    message=f"A cashier's check in the amount of ${self.check_amount} "
                                            f"will be ready for pickup at your home branch "
                                            f"on the following date: {date}. More details were sent to the following "
                                            f"address: {self.user.email}")
            # Change the user's account info and return to summary page.
            self.write_to_user(self.user)
            self.back_to_summary()
