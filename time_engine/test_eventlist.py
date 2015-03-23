import datetime
import unittest

from calc_eventlist import EventList

class TimetableTest(unittest.TestCase):

    def testLessonCount(self):
        """ test that the generated number of lessons equals the number  input"""
        form_data = {
            'start_date': datetime.date(2015, 2, 6),
            'start_time': datetime.time(4, 20),
            'name': 'test', 
            'color': 'green',
            'event_count': 15,
            'has_monday': True,
            'has_tuesday': True,
            'has_wednesday': True, 
            'has_thursday': False,
            'has_friday': False,
            'has_saturday': False, 
            'has_sunday': False
        }
        
        el = EventList(form_data)
        result = el.get_eventlist()
        self.assertEqual(15, len(result))
        
if __name__ == "__main__":
    unittest.main()  
   