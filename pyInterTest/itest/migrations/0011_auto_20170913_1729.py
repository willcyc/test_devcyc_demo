# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0010_testcasemodel_valuepicker'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicassertmodel',
            name='key',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='publicassertmodel',
            name='value',
            field=models.TextField(default=''),
        ),
    ]
