# Generated by Django 3.1.1 on 2021-04-03 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kita_representative', '0002_auto_20201121_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitarepresentative',
            name='created_at',
            field=models.DateField(auto_created=True, default=datetime.datetime.now),
        ),
    ]