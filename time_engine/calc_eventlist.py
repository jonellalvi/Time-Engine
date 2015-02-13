import datetime


class EventList(object):
    '''
    Makes a timetable, which is a list of dates,
    based on data from the form (form_data)
    '''


    def __init__(self, form_data=None):
        '''
        Return a Timetable object.
        '''
        # Initialize from any supplied form data
        print "this is form_data in calc_events: ", form_data
        if form_data:
            self.name = form_data.get('name')
            self.display_color = form_data.get('color')

            # number of events/lessons:
            self.lesson_count = form_data.get('event_count')

            # datetime.time
            self.start_time = form_data.get('start_time')

            # datetime.datetime
            self.start_date = form_data.get('start_date')

            # Save the day availability into a list starting with Monday
            self.available_days = []
            self.available_days.append(True if form_data.get('has_monday') else False)
            self.available_days.append(True if form_data.get('has_tuesday') else False)
            self.available_days.append(True if form_data.get('has_wednesday') else False)
            self.available_days.append(True if form_data.get('has_thursday') else False)
            self.available_days.append(True if form_data.get('has_friday') else False)
            self.available_days.append(True if form_data.get('has_saturday') else False)
            self.available_days.append(True if form_data.get('has_sunday') else False)

    # create the timetable
    def get_eventlist(self):
        # set an empty list that will become the timetable
        timetable = []

        # get the next day
        a_day = datetime.timedelta(days=1)

        # figure out the first valid date:
        if self.available_days[self.start_date.weekday()]:
            # if available, add to timetable
            timetable.append(self.start_date)

        # get the next date
        next_date = self.start_date + a_day

        print "The next day should be: ", self.start_date + a_day
        print "This is timetable: ", timetable

        # if there's still lessons/event to assign, keep going
        while self.lesson_count > 0:

            # check if the date is available
            if self.available_days[next_date.weekday()]:
                # add it to the timetable
                timetable.append(next_date)

                # decrement the number of lessons/events
                self.lesson_count -= 1

            # increment the date
            print "This is a_day: ", a_day
            next_date += a_day

        date_strings = [dt.strftime("%A %B %d, %Y") for dt in timetable]
        print "this is date_strings: ", date_strings
        return timetable
        # date_strings = [dt.strftime("%A %B %d, %Y") for dt in timetable]
        # return date_strings

    # create the timetable

#form_data = {'has_thursday': False, 'name': u'new_date', 'color': u'green', 'start_time': datetime.time(4, 20), 'has_tuesday': True, 'has_saturday': False, 'has_wednesday': True, 'lesson_count': 13, 'has_sunday': False, 'has_monday': True, 'has_friday': False, 'start_date': datetime.date(2015, 2, 6)}


