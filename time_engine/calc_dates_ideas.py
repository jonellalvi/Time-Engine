

# This is from http://pymotw.com/2/calendar/
# calculate the second thursday of each month
# and print the meeting date of each month.

import calendar
import pprint

pprint.pprint(calendar.monthcalendar(2007, 7))
# Notice that some days are 0. Those are days of the week
# that overlap with the given month but which are part of another month.
# Example: Assuming the second Thursday of every month,
# we can use the 0 values
# to tell us whether the Thursday of the first week is included in the
# month (or if the month starts, for example on a Friday).

# Show every month
for month in range(1, 13):

    # Compute the dates for each week that overlaps the month
    c = calendar.monthcalendar(2015, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]

    # If there is a Thursday in the first week, the second Thursday
    # is in the second week.  Otherwise the second Thursday must
    # be in the third week.
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]

    print '%3s: %2s' % (month, meeting_date)