# Generated by Django 4.0.3 on 2022-04-19 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_bot', '0008_alter_participant_puuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='perks',
            field=models.JSONField(null=True),
        ),
    ]