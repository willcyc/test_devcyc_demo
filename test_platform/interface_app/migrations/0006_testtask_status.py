# Generated by Django 2.1.1 on 2018-11-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0005_auto_20181128_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtask',
            name='status',
            field=models.IntegerField(default=0, verbose_name='状态'),
        ),
    ]
