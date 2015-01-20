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

# set some sampl data:

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


