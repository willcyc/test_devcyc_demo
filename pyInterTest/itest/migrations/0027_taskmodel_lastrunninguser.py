# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-18 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0026_auto_20171016_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='lastRunningUser',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
