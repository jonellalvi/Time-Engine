from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Questions: nullable date field, how to reference the built-in User model

class Settings(models.Model):
    ical_url = models.URLField(max_length=400)

class TimeTable(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=6, default='000000')
    creation_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User)
    lesson_count = models.IntegerField(default=0)
    has_saturday = models.BooleanField(default=False)
    has_monday = models.BooleanField(default=False)
    has_tuesday = models.BooleanField(default=False)
    has_wednesday = models.BooleanField(default=False)
    has_thursday = models.BooleanField(default=False)
    has_friday = models.BooleanField(default=False)
    has_sunday = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Result(models.Model):
    lesson_num = models.IntegerField()
    lesson_date = models.DateField()
    timetable = models.ForeignKey(TimeTable)
