from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

# Create your models here.
# Questions: nullable date field, how to reference the built-in User model

class Settings(models.Model):
    ical_url = models.URLField(max_length=400)

class TimeTable(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=6, default='009900')
    creation_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User)
    event_count = models.IntegerField(default=0)
    has_saturday = models.BooleanField(default=False)
    has_monday = models.BooleanField(default=False)
    has_tuesday = models.BooleanField(default=False)
    has_wednesday = models.BooleanField(default=False)
    has_thursday = models.BooleanField(default=False)
    has_friday = models.BooleanField(default=False)
    has_sunday = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    # Add a method to calculate the TimeTable


class Result(models.Model):
    lesson_num = models.IntegerField()
    lesson_date = models.DateField()
    timetable = models.ForeignKey(TimeTable)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance
    user = models.OneToOneField(User)

    #The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    calendar = models.URLField(max_length=400, blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class MyUser(models.Model):
    user = User
    favorite_color = models.CharField(max_length=6);