# Generated by Django 4.0.3 on 2022-08-05 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_bot', '0032_remove_runes_rune_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='stat',
            field=models.JSONField(null=True),
        ),
    ]