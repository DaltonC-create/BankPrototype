"""
This class establishes users' account information to access and interact with the software.
"""


class User:

    # Constructor.
    def __init__(self, username, password, first_name, last_name, email, checking,
                 savings, address, zip_code, city, state):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.checking = checking
        self.savings = savings
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.state = state
