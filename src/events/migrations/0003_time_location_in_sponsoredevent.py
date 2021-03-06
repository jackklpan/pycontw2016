# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-06 07:43
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import make_aware

import django.db.models.deletion


DEFAULT_TIME_ARGS = {
    (2016, 6, 3): [
        (8, 20),  (9, 20),  (9, 30),  (10, 30), (11, 0),  (11, 25), (11, 30),
        (11, 55), (13, 0),  (14, 0),  (14, 10), (14, 35), (15, 5),  (15, 50),
        (16, 0),  (16, 45),
    ],
    (2016, 6, 4): [
        (8, 0),   (8, 50),  (9, 0),   (10, 0),  (10, 30), (10, 55), (11, 0),
        (11, 25), (11, 30), (11, 55),
        (13, 0),  (13, 45), (13, 55), (14, 40), (14, 45), (15, 15), (16, 15),
        (16, 20), (16, 45), (16, 55), (17, 40), (21, 0),
    ],
    (2016, 6, 5): [
        (8, 0),   (8, 50),  (9, 0),   (10, 0),  (10, 30), (10, 55), (11, 0),
        (11, 25), (11, 30), (11, 55),
        (13, 0),  (14, 0),  (14, 10), (15, 40), (16, 0),
    ],
}


def add_default_times(apps, schema_editor):
    Time = apps.get_model('events', 'Time')
    db_alias = schema_editor.connection.alias
    Time.objects.using(db_alias).bulk_create([
        Time(value=make_aware(datetime.datetime.combine(
            datetime.date(*date_args), datetime.time(*time_args),
        )))
        for date_args, time_args_list in DEFAULT_TIME_ARGS.items()
        for time_args in time_args_list
    ])


def remove_default_times(apps, schema_editor):
    Time = apps.get_model('events', 'Time')
    db_alias = schema_editor.connection.alias
    values = [
        make_aware(datetime.datetime.combine(
            datetime.date(*date_args), datetime.time(*time_args),
        ))
        for date_args, time_args_list in DEFAULT_TIME_ARGS.items()
        for time_args in time_args_list
    ]
    Time.objects.using(db_alias).filter(value__in=values).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_sponsoredevent_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('value', models.DateTimeField(primary_key=True, serialize=False, verbose_name='value')),
            ],
            options={
                'verbose_name_plural': 'times',
                'ordering': ['value'],
                'verbose_name': 'time',
            },
        ),
        migrations.RunPython(
            code=add_default_times,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddField(
            model_name='sponsoredevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AddField(
            model_name='sponsoredevent',
            name='begin_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='begined_sponsoredevent_set', to='events.Time', verbose_name='begin time'),
        ),
        migrations.AddField(
            model_name='sponsoredevent',
            name='end_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ended_sponsoredevent_set', to='events.Time', verbose_name='end time'),
        ),
    ]
