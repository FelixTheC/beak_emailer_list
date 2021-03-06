# Generated by Django 3.1.1 on 2020-09-20 18:23

from django.db import migrations, models
import django.db.models.deletion
import emailer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kita', '0001_initial'),
        ('kita_representative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('sent', models.BooleanField(blank=True, default=False, null=True)),
                ('greeting', models.ForeignKey(blank=True, default=emailer.models.EmailSignature.get_signature, null=True, on_delete=django.db.models.deletion.SET_NULL, to='emailer.emailsignature')),
                ('kitas', models.ManyToManyField(related_name='kitas', related_query_name='kita', to='kita.Kita')),
                ('representatives', models.ManyToManyField(related_name='parents', related_query_name='parent', to='kita_representative.KitaRepresentative')),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
