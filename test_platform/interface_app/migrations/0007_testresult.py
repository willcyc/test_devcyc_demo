# Generated by Django 2.1.1 on 2018-12-13 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0006_testtask_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('error', models.IntegerField(verbose_name='错误用例')),
                ('failures', models.IntegerField(verbose_name='失败用例')),
                ('skipped', models.IntegerField(verbose_name='跳过用例')),
                ('tests', models.IntegerField(verbose_name='用例总数')),
                ('run_time', models.FloatField(verbose_name='运行时长')),
                ('result', models.TextField(default='', verbose_name='详细')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface_app.TestTask')),
            ],
        ),
    ]
