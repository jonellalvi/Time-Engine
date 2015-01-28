import calendar
import datetime
from datetime import timedelta


# set some sample data:
# form_data = {
#     'has_thursday': False,
#     'name': u'Test',
#     'color': u'green',
#     'start_time': datetime.time(4, 20),
#     'has_tuesday': False,
#     'has_saturday': False,
#     'has_wednesday': True,
#     'lesson_count': 20,
#     'has_sunday': False,
#     'has_monday': False,
#     'has_friday': True,
#     'start_date': datetime.date(2015, 2, 4)
# }

#form_data = {'has_thursday': False, 'name': u'new_date', 'color': u'green', 'start_time': datetime.time(4, 20), 'has_tuesday': True, 'has_saturday': False, 'has_wednesday': True, 'lesson_count': 13, 'has_sunday': False, 'has_monday': True, 'has_friday': False, 'start_date': datetime.date(2015, 2, 6)}

# make this into a class
class Timetable(object):
    '''
    Makes a timetable, which is a list of dates,
    based on data from the form (form_data)
    '''

    def __init__(self):
        '''
        Return a Timetable object.
        '''
        pass

    def get_start_date(self, form_data):
        '''
        Takes the data from the form and extracts the date
        the timetable should begin.
        :param form_data: data from the form
        :return: the start date as a date object
        '''
        return form_data.get('start_date')

    def get_event_time(self, form_data):
        '''
        Takes the form data and extracts the time of day
        at which the events in the timetable will occur.
        :param form_data: data from the form
        :return: the start time as a time object
        '''
        return form_data.get('start_time')

    def get_lesson_count(self, form_data):
        '''
        Takes the form data and extracts the number of
        events which occur in the timetable.
        :param form_data:
        :return: the number of events
        '''
        return form_data.get('lesson_count')

        # get the available days:
        # self.has_monday = form_data.get('has_monday')
        # self.has_tuesday = form_data.get('has_tuesday')
        # self.has_wednesday = form_data.get('has_wednesday')
        # self.has_thursday = form_data.get('has_thursday')
        # self.has_friday = form_data.get('has_friday')
        # self.has_saturday = form_data.get('has_saturday')
        # self.has_sunday = form_data.get('has_sunday')


    def get_start_day(self, start_date):
        '''
        figure out what day of the week start_date is
         :param: start_date datetime object
        :return: start date
        '''
        self.start_day = start_date.weekday()
        print self.start_day
        print start_date.strftime('%A')
        return self.start_day


    # create a function to convert the available days into the index numbers:

    # Make a list of booleans that represent which days of the week are
    # available for lessons/events
    # index 0 is monday and index 6 is sunday
    # so if avail on Mon. Wed. Fri.
    # return: [True, False, True, False, True, False, False]
    def is_available(self):
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

    def get_timetable(self, lesson_count, start_date):
        # set up some stuff:
        # gets the next day
        a_day = datetime.timedelta(days=1)
        # set an empty list that will become the timetable
        timetable = []
        # get the list of available days from is_available()
        available = self.is_available()
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
        return date_strings

    # create the timetable
    get_timetable(self, lesson_count, start_date)


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


