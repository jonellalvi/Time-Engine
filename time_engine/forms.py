from django import forms
from django.contrib.auth.models import User
from time_engine.models import TimeTable, UserProfile
from django.forms.extras.widgets import SelectDateWidget
from django.forms import widgets
from datetime import datetime
from django.forms.widgets import DateInput, TimeInput, NumberInput, CheckboxInput, CheckboxSelectMultiple, HiddenInput
from django.forms.extras.widgets import SelectDateWidget
#
# class PlanForm(forms.ModelForm):
# name = forms.CharField(max_length=200, help_text="Enter a Plan name.")
#
# Using ModelForms:
# class TimeTableForm(forms.ModelForm):
# class Meta:
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

# Hard coded for now; refactor later
YEAR_CHOICES = ('2015', '2016', '2017', '2018', '2019', '2020')


class TimeTableForm(forms.Form):
    name = forms.CharField(
        label='Name Your TimeTable',
        widget=forms.TextInput(attrs={'id': 'name', 'class': 'red'}),
        max_length=100
    )
    color = forms.ChoiceField(
        label='Choose a color',
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'color_choice'}),
        choices=COLOR_CHOICES
    )
    start_date = forms.DateField(
        label='Start Date',
        # widget=DateInput(format="%d/%m/%Y", attrs={'class': 'start_date'}),
        widget=SelectDateWidget(None, YEAR_CHOICES),
        initial=datetime.now()
        #input_formats=["%m/%d/%Y"]
    )
    start_time = forms.TimeField(
        label='Start Time (HH:MM)',
        widget=forms.TimeInput(format='%H:%M', attrs={'class': 'start_time'})
    )
    event_count = forms.IntegerField(
        label='Number of lessons',
        widget=NumberInput(attrs={'class': 'lesson_count'})
    )
    # might want to use CheckboxSelectMultiple widget for all of these guys
    # https://docs.djangoproject.com/en/1.7/ref/forms/widgets/#radioselect

    # avail_days = forms.MultipleChoiceField(
    #     label='Choose Available Days:',
    #     required=False,
    #     widget=CheckboxSelectMultiple(),
    #     choices=DAY_CHOICES
    # )

    has_saturday = forms.BooleanField(
        label='Sat',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_saturday'})
    )
    has_monday = forms.BooleanField(
        label='Mon',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_monday'})
    )
    has_tuesday = forms.BooleanField(
        label='Tue',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_tuesday'})
    )
    has_wednesday = forms.BooleanField(
        label='Wed',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_wednesday'})
    )
    has_thursday = forms.BooleanField(
        label='Thu',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_thursday'})
    )
    has_friday = forms.BooleanField(
        label='Fri',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_friday'})
    )
    has_sunday = forms.BooleanField(
        label='Sun',
        required=False,
        widget=CheckboxInput(attrs={'class': 'has_sunday'})
    )
    save = forms.CharField(
        required=False,
        widget=HiddenInput(attrs={'class': 'save'})
    )