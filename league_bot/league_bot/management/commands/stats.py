import pandas as pd
import django_subcommands

from django.core.management.base import BaseCommand
from league_bot.models import Test
from league_bot.ingest_functions.save_tables import ingest_tables
from django.db.utils import IntegrityError
from league_bot.models import Match, Participant
from league_bot.stat_functions import champ_group

def find_champ_winrate(part_table):
    part_table['win'] = part_table['win'].astype(int)
    champ_win_count_df = part_table.groupby(['champ_name'])['win'].sum()
    champ_game_count_df = part_table.groupby(['champ_name'])['win'].count()
    champ_winrate = champ_win_count_df / champ_game_count_df

    return champ_winrate


class Test(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):

        champ_group.champ_winrate()
        pass

class Command(django_subcommands.SubCommands):
    subcommands = {"test": Test}