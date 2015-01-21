import datetime
from datetime import timedelta
import calendar
# User inputs data on the form in TimeTableForm
# Take that input and process it here to figure out the dates
# Problem -- what format is the data?
# {
            #   'has_thursday': False,
            #   'name': u'Spam',
            #   'color': u'yellow',
            #   'start_time': datetime.time(4, 20),
            #   'has_tuesday': False,
            #   'has_saturday': False,
            #   'has_wednesday': True,
            #   'lesson_count': 14,
            #   'has_monday': True,
            #   'has_friday': True,
            #   'start_date': datetime.date(2000, 3, 25)
            # }
# Problem --> what output do I want to create?
# probably a list of dates and times?

# set some sample data:

form_data = {
    'has_thursday': False,
    'name': u'Test',
    'color': u'green',
    'start_time': datetime.time(4, 20),
    'has_tuesday': False,
    'has_saturday': False,
    'has_wednesday': True,
    'lesson_count': 20,
    'has_sunday': False,
    'has_monday': True,
    'has_friday': True,
    'start_date': datetime.date(2010, 5, 3)
}

#create an empty list that will hold the dates
# that comprise the timetable:
time_table = []

# get the start date and time
start_date = form_data.get('start_date')
start_time = form_data.get('start_time')
print start_date, start_time

# get the lesson count
lesson_count = form_data.get('lesson_count')

# get the available days:
# i think this is an index?
has_monday = form_data.get('has_monday')
has_tuesday = form_data.get('has_tuesday')
has_wednesday = form_data.get('has_wednesday')
has_thursday = form_data.get('has_thursday')
has_friday = form_data.get('has_friday')
has_saturday = form_data.get('has_saturday')
has_sunday = form_data.get('has_sunday')

print has_monday
print has_tuesday
print has_wednesday
print has_thursday
print has_friday
print has_saturday
print has_sunday

# now make them the indexes for the week:


# figure out what day of the week start_date is:
start_day = start_date.weekday()
print start_day
# print start_date.strftime('%A')
# create a function to convert the available days into the index numbers:

# This is blowing my head off! trying to make a list of monday through Sunday of the available days. argh.
# i need help

def is_available():
    days_of_week = []
    for key, value in form_data.iteritems():
        print  key, value
        # make a list of the available days

        if 'has' in key:
            if 'monday' in key:
                days_of_week.insert(0, value)
            if 'tuesday' in key:
                days_of_week.insert(1, value)
            if 'wednesday' in key:
                days_of_week.insert(2, value)
            if 'thursday' in key:
                days_of_week.insert(3, value)
            if 'friday' in key:
                days_of_week.insert(4, value)
            if 'saturday' in key:
                days_of_week.insert(5, value)
            if 'sunday' in key:
                days_of_week.insert(6, value)

    print days_of_week

is_available()


# loop through the number of events (i.e. 20)
# test if the date is available or not
# if it is, add the date to the list
# if not, go to the next day.

# I need to write something to get the available days. hmmm




