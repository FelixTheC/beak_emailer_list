# Generated by Django 3.1.1 on 2021-04-03 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kita_friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kitafriends',
            options={'get_latest_by': 'created_at', 'ordering': ['-kita', '-name', '-first_name'], 'verbose_name': 'Kita-Friend', 'verbose_name_plural': 'Kita-Friends'},
        ),
    ]
