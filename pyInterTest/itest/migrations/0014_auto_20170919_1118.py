# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0013_testsuitemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsuitemodel',
            name='preCases',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='testsuitemodel',
            name='valuePicker',
            field=models.TextField(default=''),
        ),
    ]
