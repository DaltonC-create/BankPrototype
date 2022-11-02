"""
This class establishes the window to transfer funds between accounts.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app import App


class TransferPage(App):

    # Constructor.
    def __init__(self, user, summary_page):
        super().__init__()
        self.root = self
        self.title("Transfer Money")
        self.user = user
        self.summary_page = summary_page
        # List of possible accounts.
        self.accounts = ["Checking", "Savings"]

        # Account label.
        self.account_title = tk.Label(self.root, text=f"{self.user.first_name} {self.user.last_name}'s Account",
                                      font=self.text_font)

        # Main frame.
        self.main_frame = tk.Frame(self.root)
        # Add space between widgets.
        self.main_frame.columnconfigure(1, weight=1, minsize=20)

        # Transfer from widgets.
        self.from_label = tk.Label(self.main_frame, text="From:")
        self.transfer_from = ttk.Combobox(self.main_frame, values=self.accounts, state="readonly", width=10)

        # Transfer to widgets.
        self.to_label = tk.Label(self.main_frame, text="To:")
        self.transfer_to = ttk.Combobox(self.main_frame, values=self.accounts, state="readonly", width=10)

        # Dollar amount widgets.
        self.amount_label = tk.Label(self.main_frame, text="Amount:")
        self.amount_entry = tk.Entry(self.main_frame, width=14)

        # Button widgets for submitting transfer and returning to the summary page.
        self.button_frame = tk.Frame(self.root)
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.verify_transfer)
        self.back_button = tk.Button(self.button_frame, text="Back to Summary", command=self.back_to_summary)

        self.setup_transfer_page()

    # Sets up locations of widgets for transfer page window.
    def setup_transfer_page(self):
        # Account name title.
        self.account_title.pack(anchor=tk.CENTER)

        # Main frame.
        self.main_frame.pack(anchor=tk.CENTER, pady=20)

        # From account row.
        self.from_label.grid(column=0, row=0)
        self.transfer_from.grid(column=1, row=0)
        # Set default value for transfer from combobox.
        self.transfer_from.current(0)

        # To account row.
        self.to_label.grid(column=0, row=1, pady=10)
        self.transfer_to.grid(column=1, row=1, pady=10)
        # Set default value for transfer to combobox.
        self.transfer_to.current(1)

        # Set functions when values are selected from each combo box to alternate between choices.
        self.transfer_from.bind("<<ComboboxSelected>>", self.change_transfer_to)
        self.transfer_to.bind("<<ComboboxSelected>>", self.change_transfer_from)

        # Dollar amount row.
        self.amount_label.grid(column=0, row=2)
        self.amount_entry.grid(column=1, row=2)

        # Submit and back buttons row.
        self.button_frame.pack(anchor=tk.CENTER)
        self.submit_button.pack(side="left", padx=5)
        self.back_button.pack(side="left", padx=5)

    # Verifies the transfer amount and accounts.
    def verify_transfer(self):
        # Transfer amount is not a valid number.
        if not self.is_float(self.amount_entry.get()):
            messagebox.showerror(title="Invalid amount", message="The transfer amount is not a valid number.")
            self.focus()
        # Transfer amount is a valid number.
        else:
            transfer_amount = "{:.2f}".format(float(self.amount_entry.get()))
            from_account = self.transfer_from.get()

            # Check if funds will be transferred from checking & is less than current amount.
            if from_account == self.accounts[0] and float(transfer_amount) <= float(self.user.checking):
                self.user.checking -= float(transfer_amount)
                self.user.savings += float(transfer_amount)
                # Update csv file.
                self.write_to_user(self.user)
                self.back_to_summary()
            # Check if funds will be transferred from savings & is less than current amount.
            elif from_account == self.accounts[1] and float(transfer_amount) <= float(self.user.savings):
                self.user.checking += float(transfer_amount)
                self.user.savings -= float(transfer_amount)
                # Update csv file.
                self.write_to_user(self.user)
                self.back_to_summary()
            # Transfer amount is larger than funds in the account.
            else:
                messagebox.showerror(title="Invalid amount", message="The transfer amount is too high")
                self.focus()

    # Changes the value for transfer_to when transfer_from is changed, parameter e is the event listener.
    def change_transfer_to(self, e):
        if self.transfer_from.get() == self.accounts[0]:
            self.transfer_to.current(1)
        else:
            self.transfer_to.current(0)

    # Changes the value for transfer_from when transfer_to is changed, parameter e is the event listener.
    def change_transfer_from(self, e):
        if self.transfer_to.get() == self.accounts[0]:
            self.transfer_from.current(1)
        else:
            self.transfer_from.current(0)

    # Returns to the summary page.
    def back_to_summary(self):
        # Destroys current window and refreshes summary page in case of changes.
        self.root.destroy()
        self.summary_page.refresh()
