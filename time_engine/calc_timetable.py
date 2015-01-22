import calendar
import datetime
from datetime import timedelta


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
    'has_monday': False,
    'has_friday': True,
    'start_date': datetime.date(2015, 2, 4)
}

# create an empty list that will hold the dates
# that comprise the timetable:
time_table = []

# get the start date and time
start_date = form_data.get('start_date')
start_time = form_data.get('start_time')
print start_date, start_time

# get the lesson count
lesson_count = form_data.get('lesson_count')

# get the available days:
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

# Make a list of booleans that represent which days of the week are
# available for lessons/events
# index 0 is monday and index 6 is sunday
# so if avail on Mon. Wed. Fri.
# return: [True, False, True, False, True, False, False]
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


# loop through the number of events (i.e. 20)
# test if the date is available or not
# if it is, add the date to the list
# if not, go to the next day.

def get_timetable(lesson_count, start_date):
    # set up some stuff:

    # gets the next day
    a_day = datetime.timedelta(days=1)

    # set an empty list that will become the timetable
    timetable = []

    # get the list of available days from is_available()
    available = is_available()

    # figure out the first valid date:
    if available[start_date.weekday()]:
        # if avail, add to the timetable
        timetable.append(start_date)

    # get the next date
    next_date = start_date + a_day

    print "The next day should be: ", start_date + a_day

    # if there's still lessons/event to assign, keep going
    while lesson_count > 0:
        # check if the date is available
        if available[next_date.weekday()]:
            # add it to the timetable
            timetable.append(next_date)
            # increment the date
            next_date += a_day
            # decrement the number of lessons/events
            lesson_count -= 1
        else:
            #if the date isn't available,
            # just increment the date
            next_date += a_day

    print timetable
    date_strings = [dt.strftime("%A %B %d, %Y") for dt in timetable]
    print date_strings

# create the timetable
get_timetable(lesson_count, start_date)


# ---------------------------------------------------------------------
#
#         # -- Add a day to the last date
#         next_date = timetable[-1] + datetime.timedelta(days=1)
#
#         if date_is_available(next_date, valid_days):
#             timetable.append(next_date)
#             lesson_count -= 1
#
#         days_scanned += 1
#         if days_scanned > 365 * 2:
#         # return error that we looked 2 years into the future & could not schedule all the dates...
#             pass
#     return timetable


