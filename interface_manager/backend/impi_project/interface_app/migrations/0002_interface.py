# Generated by Django 2.1.1 on 2019-04-02 12:36

from django.db import migrations, models
import django.db.models.deletion
import interface_app.fields.model.object_field
import interface_app.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description')),
                ('host', models.CharField(default='', max_length=200, verbose_name='host')),
                ('url', models.CharField(max_length=500, verbose_name='url')),
                ('method', models.CharField(max_length=20, verbose_name='method')),
                ('header', interface_app.fields.model.object_field.ObjectField(default={}, verbose_name='header')),
                ('parameter', interface_app.fields.model.object_field.ObjectField(default={}, verbose_name='parameter')),
                ('parameter_type', models.CharField(default='json', max_length=20, verbose_name='parameter_type,json or form')),
                ('response', interface_app.fields.model.object_field.ObjectField(default='', verbose_name='response')),
                ('response_type', models.CharField(default='json', max_length=20, verbose_name='response_type,json or html')),
                ('assertion', interface_app.fields.model.object_field.ObjectField(default={}, verbose_name='assertion')),
                ('service', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='service_interfaces', to='interface_app.Service')),
            ],
            bases=(models.Model, interface_app.models.base.Base),
        ),
    ]
