# import the datetime module
import datetime


# this class generates timetables from lists of dates

class EventList(object):
    """
    Makes a timetable, which is a list of dates,
    based on data from the form (form_data)
    """

    # The init method accepts the data from the form as an argument.
    # form_data defaults to None if no argument is passed to the method.
    def __init__(self, form_data=None):
        """
        Extract form data and create a list of valid days.
        """

        # Initialize from any supplied form data
        # This is a check to make sure some data was passed in.
        # print "this is form_data in calc_events: ", form_data

        # if there is form_data extract the information from the form.
        if form_data:
            # name of the timetable and the color:
            self.name = form_data.get('name')
            self.display_color = form_data.get('color')

            # number of events/lessons:
            self.lesson_count = form_data.get('event_count')

            # datetime.time, the start time for all events
            self.start_time = form_data.get('start_time')

            # datetime.datetime, the start date for all events
            self.start_date = form_data.get('start_date')

            # Save the day availability into a list starting with Monday
            # First create an empty list
            self.available_days = []
            # Now append to the list a set of boolean values
            # For the days that were checked on the form,
            # Append True in the corresponding location in the list
            # Otherwise append False
            # Position in the list dictates the day of the week: 0 = Monday, 6th = Sunday
            self.available_days.append(True if form_data.get('has_monday') else False)
            self.available_days.append(True if form_data.get('has_tuesday') else False)
            self.available_days.append(True if form_data.get('has_wednesday') else False)
            self.available_days.append(True if form_data.get('has_thursday') else False)
            self.available_days.append(True if form_data.get('has_friday') else False)
            self.available_days.append(True if form_data.get('has_saturday') else False)
            self.available_days.append(True if form_data.get('has_sunday') else False)


    def get_eventlist(self):
        """
        Returns the list of valid dates
        """

        # Holds list of valid dates
        timetable = []

        # Time difference of a day.
        a_day = datetime.timedelta(days=1)

        # Determine the first valid date
        # Convert the start_date to a number using weekday()
        # and see if the value in the list for that day is True.
        if self.available_days[self.start_date.weekday()]:
            # if it's True, i.e. available, add it to the timetable
            # if it's False, don't do anything.
            timetable.append(self.start_date)

        # Get the next date
        next_date = self.start_date + a_day

        # sanity check
        # print "The next day should be: ", self.start_date + a_day
        # print "This is timetable: ", timetable

        # if there's still events to assign,
        # keep appending dates to the timetable
        while self.lesson_count > 0:

            # check if the date is available
            if self.available_days[next_date.weekday()]:
                # add it to the timetable
                timetable.append(next_date)

                # decrement the number of lessons/events
                self.lesson_count -= 1

            # increment the date.
            next_date += a_day

        # return the finished list of dates.
        return timetable


# An example of what form_data might look like
# form_data = {'has_thursday': False, 'name': u'new_date', 'color': u'green', 'start_time': datetime.time(4, 20), 'has_tuesday': True, 'has_saturday': False, 'has_wednesday': True, 'lesson_count': 13, 'has_sunday': False, 'has_monday': True, 'has_friday': False, 'start_date': datetime.date(2015, 2, 6)}


