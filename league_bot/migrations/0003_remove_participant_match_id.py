# Generated by Django 4.0.3 on 2022-04-10 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league_bot', '0002_match_participant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='match_id',
        ),
    ]