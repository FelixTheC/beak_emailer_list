# Generated by Django 3.1.1 on 2021-04-15 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedulecommander',
            options={'ordering': ('earliest_execution_date',)},
        ),
    ]