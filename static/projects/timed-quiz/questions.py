__author__ = 'student'
class Question:
    answer = None
    text = None


class Add(Question):
    def __init__(self, num1, num2):
        self.text = '{} + {}'.format(num1, num2)
        self.answer = num1 + num2


class Multiply(Question):
    def __init__(self, num1, num2):
        self.text = '{} x {}'.format(num1, num2)
        self.answer = num1 * num2


class Subtract(Question):
    def __init__(self, num1, num2):
        # need to check which is larger and which is smaller:
        if num1 < num2:
            # use tuple packing and unpacking to swap the values
            # so that num1 becomes the larger value:
            num1, num2 = num2, num1

        # create the equation for the user
        self.text = '{} - {}'.format(num1, num2)
        self.answer = num1 - num2