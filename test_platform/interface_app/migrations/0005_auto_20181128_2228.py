# Generated by Django 2.1.1 on 2018-11-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0004_testtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtask',
            name='cases',
            field=models.TextField(default='', verbose_name='关联用例'),
        ),
    ]
