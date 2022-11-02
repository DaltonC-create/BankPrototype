"""
This class establishes the window to schedule appointments.
NOTE: Will need to import tkcalendar module to run.
"""
import datetime as dt
import tkcalendar as cal
import tkinter as tk
from tkinter import ttk, messagebox
from app import App


# Returns the first day of selection in the calendar (Always a weekday).
def set_start_day():
    start_day = dt.datetime.today() + dt.timedelta(days=1)
    # If tomorrow is a weekend day, increment to the following Monday.
    if start_day.weekday() == 5:
        start_day += dt.timedelta(days=2)
    elif start_day.weekday() == 6:
        start_day += dt.timedelta(days=1)
    return start_day


class ScheduleAppointmentPage(App):

    # Constructor.
    def __init__(self, user, summary_page):
        super().__init__()
        self.root = self
        # Set window parameters.
        self.title("Schedule Appointment")
        self.height = 650
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))

        self.user = user
        self.summary_page = summary_page
        # Time list for combobox selection.
        self.times = ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "2:00 PM", "2:30 PM",
                      "3:00 PM", "3:30 PM", "4:00 PM"]
        # Types of meetings for combobox.
        self.meeting_types = ["In person", "Virtual"]
        # List comprehension to get advisors first names for combobox.
        self.advisor_names = [i.first_name for i in self.advisors]

        # Variable to hold selected advisor.
        self.advisor = None

        # Get tomorrow's date for start of appointment options, unless it's a weekend.
        self.tomorrow = set_start_day()
        # Date variables for calendar.
        self.year = self.tomorrow.year
        self.month = self.tomorrow.month
        self.day = self.tomorrow.day
        # Previous day selected for calendar widget when error occurs.
        self.day_before_selection = self.tomorrow
        # Max date, 30 days after start date.
        self.max_date = self.tomorrow + dt.timedelta(days=20)

        # Calendar widget.
        self.calendar = cal.Calendar(self.root, selectmode="day", year=self.year, month=self.month, day=self.day,
                                     mindate=self.tomorrow, maxdate=self.max_date, showweeknumbers=False,
                                     font=self.text_font, firstweekday="sunday")

        # Hours label at the top of the page.
        self.hours_label = tk.Label(self.root, text="Regular Business Hours:\n9:00-5:00 Monday-Friday",
                                    font=self.text_font)

        # Main frame.
        self.main_frame = tk.Frame(self.root)
        # Add space between widgets.
        self.main_frame.columnconfigure(1, weight=1, minsize=20)

        # In person or virtual meeting options widgets.
        self.meeting_label = tk.Label(self.main_frame, text="Meeting Location:")
        self.meeting_combobox = ttk.Combobox(self.main_frame, values=self.meeting_types, state="readonly", width=15)

        # Advisor selection widgets.
        self.advisor_label = tk.Label(self.main_frame, text="Select Advisor:")
        self.advisor_combobox = ttk.Combobox(self.main_frame, values=self.advisor_names, state="readonly", width=15)

        # Appointment time selection widgets.
        self.time_label = tk.Label(self.main_frame, text="Appointment Time:")
        self.time_combobox = ttk.Combobox(self.main_frame, values=self.times, state="readonly", width=15)

        # Reason for appointment widgets.
        self.reason_label = tk.Label(self.main_frame, text="Reason:")
        self.reason_entry = tk.Text(self.main_frame, width=25, height=3)

        # Button widgets for submitting and returning to the summary page.
        self.button_frame = tk.Frame(self.root)
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_appointment)
        self.back_button = tk.Button(self.button_frame, text="Back to Summary", command=self.back_to_summary)

        self.setup_appointment_page()

    # Sets up locations of widgets for appointment page window.
    def setup_appointment_page(self):
        # Hours of Operation.
        self.hours_label.pack(anchor=tk.CENTER, pady=10)

        # Calendar.
        self.calendar.pack(anchor=tk.CENTER, pady=10)

        # Calendar binding.
        self.calendar.bind("<<CalendarSelected>>", self.check_day)

        self.main_frame.pack(anchor=tk.CENTER)

        # Meeting type row.
        self.meeting_label.grid(column=0, row=0, sticky="e", pady=10)
        self.meeting_combobox.grid(column=2, row=0, sticky="w", pady=10)
        # Set default value for meeting type.
        self.meeting_combobox.current(0)

        # Advisor selection row.
        self.advisor_label.grid(column=0, row=1, sticky="e")
        self.advisor_combobox.grid(column=2, row=1, sticky="w")
        # Set the default value for advisor selection.
        self.advisor_combobox.current(0)

        # Time selection row.
        self.time_label.grid(column=0, row=2, sticky="e", pady=10)
        self.time_combobox.grid(column=2, row=2, sticky="w", pady=10)
        # Set default value for time selection.
        self.time_combobox.current(0)

        # Reason for appointment row.
        self.reason_label.grid(column=0, row=3, sticky="e")
        self.reason_entry.grid(column=2, row=3, sticky="w")

        # Submit and back buttons row.
        self.button_frame.pack(anchor=tk.CENTER, pady=10)
        self.submit_button.grid(column=0, row=0, padx=5)
        self.back_button.grid(column=1, row=0, padx=5)

    # Returns to the summary page.
    def back_to_summary(self):
        # Destroys current window and refreshes summary page in case of changes.
        self.root.destroy()
        self.summary_page.refresh()

    # Checks if user selects a weekend day, parameter e is the event listener.
    def check_day(self, e):
        # Get selected day on calendar.
        current_selection = dt.datetime.strptime(self.calendar.get_date(), "%m/%d/%y")
        # Check if selected day is a Saturday.
        if current_selection.weekday() == 5 or current_selection.weekday() == 6:
            # Keep selection without changing & display error message.
            self.calendar.selection_set(self.day_before_selection)
            messagebox.showerror(title="Invalid day", message="Please only select a business day.")
        # Selection was weekday, store date to save if a weekend day is selected next.
        else:
            self.day_before_selection = current_selection

    # Returns the advisor object given the name attribute.
    def get_advisor(self):
        for i in self.advisors:
            if i.first_name == self.advisor_combobox.get():
                return i

    # Returns true if the date and time are not taken by that advisor.
    def is_available(self, date_selection, time_selection):
        for key in self.advisor.availability:
            # If advisor already has that date and time scheduled return false.
            if key == date_selection and time_selection in self.advisor.availability[key]:
                return False
        return True

    # Adds the appointment to the advisor object.
    def set_appointment(self, date, time):
        # If no appointment exists for that date.
        if date not in self.advisor.availability.keys():
            # New key and value are created, then the dictionary is sorted.
            self.advisor.availability[date] = [time]
            self.advisor.availability = dict(sorted(self.advisor.availability.items()))
        # If there is a record of that date, add the time.
        else:
            # Time is added to list of values for that date, then the list is sorted.
            self.advisor.availability[date].append(time)
            self.advisor.availability[date].sort(key=lambda x: dt.datetime.strptime(x, "%I:%M %p"))

    # Processes the appointment to be submitted.
    def submit_appointment(self):
        # Date, time, and advisor chosen by user.
        date_selection = self.calendar.get_date()
        time_selection = self.time_combobox.get()
        self.advisor = self.get_advisor()

        # Checks if date and time are available for that advisor.
        if not self.is_available(date_selection, time_selection):
            messagebox.showerror(title="Invalid Selection",
                                 message=f"{self.advisor.first_name} {self.advisor.last_name} is not available at "
                                         f"{time_selection} on {date_selection}")
            self.focus()
        else:
            # User set meeting to be in person.
            if self.meeting_combobox.get() == self.meeting_types[0]:
                messagebox.showinfo(title="Success!", message=f"Your in person meeting with {self.advisor.first_name} "
                                                              f"has been scheduled at {time_selection} on "
                                                              f"{date_selection} at your local home branch for reason: "
                                                              f"{self.reason_entry.get('1.0', tk.END)}")
            # User set meeting to be virtual.
            elif self.meeting_combobox.get() == self.meeting_types[1]:
                messagebox.showinfo(title="Success!", message=f"Your virtual meeting with {self.advisor.first_name} "
                                                              f"has been scheduled at {time_selection} on "
                                                              f"{date_selection} for reason: "
                                                              f"{self.reason_entry.get('1.0', tk.END)} "
                                                              f"You will be emailed a Zoom link 30 minutes prior to "
                                                              f"the start of the meeting.")
            # Set the appointment and apply changes to advisor's schedule.
            self.set_appointment(date_selection, time_selection)
            self.write_to_advisor()
            # Close window and return to summary.
            self.back_to_summary()
