# Generated by Django 3.0.5 on 2020-04-10 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadImage', '0004_auto_20200410_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='date_at',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 4, 10, 18, 30, 43, 499031)),
        ),
    ]
