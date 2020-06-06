# Generated by Django 2.1.1 on 2019-04-19 13:41

from django.db import migrations, models
import interface_app.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0002_interface'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('status', models.IntegerField(choices=[(0, '未执行'), (1, '正在执行'), (2, '执行完成')], default=0, verbose_name='状态')),
                ('interface', models.ManyToManyField(to='interface_app.Interface')),
            ],
            bases=(models.Model, interface_app.models.base.Base),
        ),
    ]