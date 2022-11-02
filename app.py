"""
This class establishes the driver class from which most other classes will inherit.
"""

import tkinter as tk
import datetime as dt
import csv
import employee
import user


class App(tk.Tk):

    # Constructor.
    def __init__(self):
        super().__init__()
        # Start to window dimensions for every subclass placing window in the middle of screen.
        self.text_font = ("ariel", 20, "bold")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = 550
        self.height = 400
        self.x = (self.screen_width/2) - (self.width/2)
        self.y = (self.screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
        self.date_today = dt.datetime.today().strftime("%m/%d/%y")

        # List of user accounts.
        self.users = []
        # List of advisor accounts.
        self.advisors = []

        # Open users.csv file and get list of users.
        with open("users.csv") as file:
            # Create csv reader that splits file by ",".
            user_csv = csv.reader(file, delimiter=",")
            # Skip header row.
            next(file)
            for i in user_csv:
                # Append each row of the csv file to the list of users.
                self.users.append(user.User(i[0], i[1], i[2], i[3], i[4], float(i[5]), float(i[6]), i[7], float(i[8]),
                                            i[9], i[10]))

        # Open advisor.csv and get list of advisors.
        with open("advisor.csv") as file_adv:
            adv_csv = csv.reader(file_adv, delimiter=",")
            # Skip the header row when reading.
            next(file_adv)
            for i in adv_csv:
                # append each row of the csv file to the list of advisors, changing final column to a dictionary.
                self.advisors.append(employee.Employee(i[0], i[1], i[2], eval(i[3])))
            self.check_availability_dates()

    # Checks if any dates have passed and deletes them from the dictionary.
    def check_availability_dates(self):
        # Loop over all rows of the list to get dictionaries.
        for row in self.advisors:
            # Loop through the keys of the dictionary as a list to delete without errors.
            for key in list(row.availability.keys()):
                if key < self.date_today:
                    del row.availability[key]
        # Check for any dates earlier than today and delete them.
        self.write_to_advisor()

    # Writes changes to advisor.csv file.
    def write_to_advisor(self):
        with open("advisor.csv", "w+", newline="") as file:
            writer = csv.writer(file)
            # Header row.
            writer.writerow(["FirstName", "LastName", "Email", "Availability"])
            # Write all attributes in advisors list back to advisor.csv file.
            for i in self.advisors:
                writer.writerow([i.first_name, i.last_name, i.email, i.availability])

    @staticmethod
    def is_float(var):
        # Return true if parameter is a float.
        try:
            float(var)
        except ValueError:
            return False
        return True

    # Writes changes to user.csv file.
    def write_to_user(self, user_obj):
        with open("users.csv", "w+", newline="") as file:
            writer = csv.writer(file)
            # Header row.
            writer.writerow(["Username", "Password", "First Name", "Last Name", "Email", "Checking", "Savings",
                             "Address", "Zip Code", "City", "State"])
            # Write all attributes in users list back to users.csv file.
            for i in self.users:
                # If row is current account signed in.
                if i.first_name == user_obj.first_name:
                    writer.writerow([user_obj.username, user_obj.password, user_obj.first_name, user_obj.last_name,
                                     user_obj.email, round(user_obj.checking, 2), round(user_obj.savings, 2),
                                     user_obj.address, user_obj.zip_code, user_obj.city, user_obj.state])
                # Every other account in list.
                else:
                    writer.writerow([i.username, i.password, i.first_name, i.last_name, i.email,
                                     round(i.checking, 2), round(i.savings, 2), i.address, i.zip_code, i.city, i.state])
