# Generated by Django 2.1.1 on 2018-11-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('url', models.TextField(default='', verbose_name='URL')),
                ('req_method', models.CharField(default='', max_length=10, verbose_name='方法')),
                ('req_type', models.CharField(default='', max_length=10, verbose_name='参数类型')),
                ('req_header', models.TextField(default='', verbose_name='头部')),
                ('req_parameter', models.TextField(default='', verbose_name='参数')),
                ('responses_assert', models.TextField(default='', verbose_name='断言')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('Module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_app.Module')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_app.Project')),
            ],
        ),
    ]
