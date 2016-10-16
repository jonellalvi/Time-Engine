# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_engine', '0002_timetable_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='start_time',
            field=models.TimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='color',
            field=models.CharField(default=b'009900', max_length=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='start_date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
