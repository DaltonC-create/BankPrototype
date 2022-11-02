"""
This class establishes accounts for employees for appointment class.
"""


class Employee:

    # Constructor.
    def __init__(self, first_name, last_name, email, availability):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.availability = availability
