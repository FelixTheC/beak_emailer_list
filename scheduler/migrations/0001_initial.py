# Generated by Django 3.1.1 on 2021-04-15 20:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleCommander',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('earliest_execution_date', models.DateTimeField()),
                ('module', models.CharField(max_length=255)),
                ('func', models.CharField(max_length=255)),
                ('args', models.CharField(max_length=255)),
                ('kwargs', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.JSONField()),
            ],
        ),
    ]
