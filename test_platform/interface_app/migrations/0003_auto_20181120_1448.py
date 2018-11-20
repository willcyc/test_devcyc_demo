# Generated by Django 2.1.1 on 2018-11-20 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0002_auto_20181107_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='responses_assert',
        ),
        migrations.AddField(
            model_name='testcase',
            name='resp_assert',
            field=models.TextField(default='', verbose_name='验证'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='req_header',
            field=models.TextField(default='', verbose_name='header'),
        ),
    ]