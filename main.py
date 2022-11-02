"""
This is a prototype for a banking application for Software Engineering class
group project by the group Silicon Wraiths.
Each class is a separate window within the GUI program, except for the user class
that establishes user account information and the employee class for financial advisors.
NOTE: Need to install tkcalendar module for check and appointment classes to run.
NOTE: Needs at least Python 3.10 to compile correctly.
"""
import login
import app


# Main function.
if __name__ == "__main__":
    app = app.App()
    login.LoginPage(app, app.users)
    app.mainloop()
