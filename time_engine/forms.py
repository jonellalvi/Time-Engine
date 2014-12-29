
from django import forms
from time_engine.models import TimeTable
#
# class PlanForm(forms.ModelForm):
#     name = forms.CharField(max_length=200, help_text="Enter a Plan name.")
#

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable