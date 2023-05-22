# Generated by Django 4.1.1 on 2022-10-01 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=150)),
                ('phone_no', models.CharField(max_length=10)),
                ('subject', models.TextField()),
                ('message', models.TextField()),
                ('contacted_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['-contacted_time'],
            },
        ),
    ]
