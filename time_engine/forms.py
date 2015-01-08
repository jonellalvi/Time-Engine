
from django import forms
from django.contrib.auth.models import User
from time_engine.models import TimeTable, UserProfile
from django.forms.extras.widgets import SelectDateWidget
from django.forms import widgets
from datetime import date
from django.forms.widgets import DateInput, TimeInput, NumberInput, CheckboxInput
#
# class PlanForm(forms.ModelForm):
#     name = forms.CharField(max_length=200, help_text="Enter a Plan name.")
#
# Using ModelForms:
# class TimeTableForm(forms.ModelForm):
#     class Meta:
#         model = TimeTable

# User Registration stuff
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'calendar')




# Using basic forms:
COLOR_CHOICES = (('blue', 'blue'),
                 ('green', 'green'),
                 ('red', 'red'),
                 ('yellow', 'yellow'))

class TimeTableForm(forms.Form):
    name = forms.CharField(label='Name Your TimeTable', widget=forms.TextInput(attrs={'id': 'tt_name'}), max_length=100)
    color = forms.MultipleChoiceField(label='Choose a color', widget=forms.RadioSelect(attrs={'class': 'color_choice'}), choices=COLOR_CHOICES)
    start_date = forms.DateField(label='Start Date', widget=DateInput(attrs={'class': 'start_date'}))
    start_time = forms.TimeField(label='Start Time', widget=TimeInput(attrs={'class': 'start_time'}))
    lesson_count = forms.IntegerField(label='Number of lessons', widget=NumberInput(attrs={'class': 'lesson_count'}))
    has_saturday = forms.BooleanField(label='Sat', widget=CheckboxInput(attrs={'class': 'has_saturday'}))
    has_monday = forms.BooleanField(label='Mon', widget=CheckboxInput(attrs={'class': 'has_monday'}))
    has_tuesday = forms.BooleanField(label='Tue', widget=CheckboxInput(attrs={'class': 'has_tuesday'}))
    has_wednesday = forms.BooleanField(label='Wed', widget=CheckboxInput(attrs={'class': 'has_wednesday'}))
    has_thursday = forms.BooleanField(label='Thu', widget=CheckboxInput(attrs={'class': 'has_thursday'}))
    has_friday = forms.BooleanField(label='Fri', widget=CheckboxInput(attrs={'class': 'has_friday'}))