# Generated by Django 4.0.3 on 2022-08-05 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league_bot', '0031_runes_rune_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runes',
            name='rune_cat',
        ),
    ]