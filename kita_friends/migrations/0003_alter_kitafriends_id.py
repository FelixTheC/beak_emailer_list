# Generated by Django 3.2 on 2021-05-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kita_friends', '0002_auto_20210403_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitafriends',
            name='id',
            field=models.BigIntegerField(db_index=True, primary_key=True, serialize=False),
        ),
    ]