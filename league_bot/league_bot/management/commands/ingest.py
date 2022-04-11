import pandas as pd
import django_subcommands

from django.core.management.base import BaseCommand
from league_bot.models import Test
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Match


def insert_match_table(match_table_row):
    match_object_row = Match.objects.create(
        # this is the match_oid but since its index it is unnamed
        match_id = match_table_row['match_id'],
        duration = match_table_row['duration'],
        start_time = match_table_row['start_time'],
        game_mode = match_table_row['game_mode'],
        patch = match_table_row['patch']
    )
    return match_object_row

class Challengers(BaseCommand):
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        match_table, part_table = ingest_tables(amount=2)
        match_dict = match_table.to_dict('records')
        for row in match_dict:
            inserted_row = insert_match_table(row)
            print(f"INSERT: {row}")
        pass

class Command(django_subcommands.SubCommands):
    subcommands = {"challengers": Challengers}

