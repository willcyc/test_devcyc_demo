# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-23 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0029_taskmodel_lastrunningresultidlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='currentResultMark',
            new_name='currentResultVersion',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='lastResultVersion',
            field=models.IntegerField(default=-1),
        ),
    ]
