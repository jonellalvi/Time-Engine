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


# figure out what day of the week start_date is:
start_day = start_date.weekday()
print start_day
print start_date.strftime('%A')
# create a function to convert the available days into the index numbers:

# This is blowing my head off! trying to make a list of monday through Sunday of the available days. argh.
# i need help

def is_available():
    available_days = []
    available_days.append(True if form_data.get('has_monday') else False)
    available_days.append(True if form_data.get('has_tuesday') else False)
    available_days.append(True if form_data.get('has_wednesday') else False)
    available_days.append(True if form_data.get('has_thursday') else False)
    available_days.append(True if form_data.get('has_friday') else False)
    available_days.append(True if form_data.get('has_saturday') else False)
    available_days.append(True if form_data.get('has_sunday') else False)

    return available_days
# [True, False, True, False, True, False, False]
is_available()


# loop through the number of events (i.e. 20)
# test if the date is available or not
# if it is, add the date to the list
# if not, go to the next day.

# starting at start_date, create the list of lessons

def get_timetable(lesson_count, start_date):
    dayDelta = datetime.timedelta(days=1)
    current_date = start_date
    # goal is to make a list of dates for the lessons
    timetable = []
    timetable.append(start_date)
    while lesson_count > 0:
        # need to start at startdate and loop through subsequent dates
        # if the date is avaialbe, add it to the list of dates
        # and decriment lesson_count
        # if the date is not available, jsut loop to the next one.
        available = is_available()
        if available[current_date.weekday()]:
            timetable.append(current_date)
            start_date += dayDelta
            lesson_count -= 1

    print timetable

get_timetable(lesson_count, start_date)

# I need to write something to get the available days. hmmm
# ---------------------------------------------------------------------
 


