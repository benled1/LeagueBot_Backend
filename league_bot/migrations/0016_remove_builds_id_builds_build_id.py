# Generated by Django 4.0.3 on 2022-07-21 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_bot', '0015_builds_champ_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builds',
            name='id',
        ),
        migrations.AddField(
            model_name='builds',
            name='build_id',
            field=models.CharField(default=0, max_length=50, primary_key=True, serialize=False),
        ),
    ]
