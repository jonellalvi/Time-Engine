
import datetime
import random

from questions import Add, Multiply, Subtract

# some things to try:

# 5. Allow the user to practice specific operators.
# 6. 

# completed:
# 4. Add subtraction questions
# 2. Make sure the user can specify the range they want the numbers to come from
# 1. Change so it takes a number of questions to generate
# 3. Add in some further stats that tell you how long it took to answer each question.


class Quiz:
    questions = []
    answers = []

    def __init__(self, q_num):
        question_types = (Add, Multiply, Subtract)
        # question_types[0](1, 5)
        # generate 10 random questions with numbers from 1 to 10
        for _ in range(q_num):
            num1 = random.randint(1, q_num)
            num2 = random.randint(1, q_num)
            question = random.choice(question_types)(num1, num2)
            # add these questions into self.questions
            self.questions.append(question)

    def take_quiz(self):
        # log the start time
        self.start_time = datetime.datetime.now()
        # ask all of the questions
        cnt = 1
        for question in self.questions:
        # log if they got the question right
            self.answers.append(self.ask(question, cnt))
            cnt += 1
        else:
            # log the end time
            self.end_time = datetime.datetime.now()
        return self.summary()


    def ask(self, question, cnt):
        correct = False
        # log the start time
        question_start = datetime.datetime.now()
        # capture the answer
        # use raw_input if using Python 2.x, input if 3.x!
        # try testing for version with import sys and
        # sys.version.split(" ")[0].sp
        answer = raw_input('Question #' + str(cnt) + ':' + ' ' + question.text + ' = ')
        # check the answer
        if answer == str(question.answer):
            correct = True
        # log the end time
        question_end = datetime.datetime.now()
        # if the answer's right, send back True
        # otherwise, send back False
        # send back the elapsed time, too
        return correct, question_end - question_start


    def total_correct(self):
        # return the total # of correct answers
        total = 0
        for answer in self.answers:
            if answer[0]:
                total += 1
        return total


    def summary(self):
        # print how many you got right and the total # of questions. 5/10
        print("You got {} out of {} right".format(
              self.total_correct(), len(self.questions)
          ))
        # print the total time for the quiz: 30 seconds!
        print("It took you {} seconds total.".format(
              (self.end_time-self.start_time).seconds
          ))
        # print the time it took for each question.
        # then loop through it and print each time.
        #print(self.answers)
        count = 1
        for answer in self.answers:
            print("It took you {} second(s) to answer question #{}. ".format(
                answer[1].seconds, count
            ))
            count += 1


# Ask for the number of questions
q_num = int(raw_input("Enter the number of questions: "))
# Create the quiz
Quiz(q_num).take_quiz()