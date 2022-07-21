from ctypes import wintypes
from distutils.command.build import build
from numpy import number
import pandas as pd
import django_subcommands

from league_bot.models import Builds, Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion, Builds
from league_bot.stat_functions.champion import get_winrate, get_play_count, get_best_builds


def create_build_entry(input_df):
    for index, row in input_df.iterrows():
        Builds.objects.create(
            champ_name = Champion.objects.get(champ_name = row['champ_name']),
            item0 = row['item0'],
            item1 = row['item1'],
            item2 = row['item2'],
            item3 = row['item3'],
            item4 = row['item4'],
            item5 = row['item5'],
            win_rate = row['win_rate']
        )
           



class Test(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        champion_records =Champion.objects.values()
        for champion in champion_records:
            get_best_builds(champion_name=champion['champ_name'])
        pass



class ChampionStats(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        champion_records =Champion.objects.values()
        for champion in champion_records:
            all_champ_part_records = Participant.objects.filter(champ_name=champion['champ_name']).values('win')

            winrate = get_winrate(all_champ_part_records)
            Champion.objects.filter(champ_name=champion['champ_name']).update(champ_winrate=winrate)

            play_count = get_play_count(all_champ_part_records=all_champ_part_records)
            Champion.objects.filter(champ_name=champion['champ_name']).update(champ_play_count=play_count)

            build_df = get_best_builds(champion_name=champion['champ_name'])
            if isinstance(build_df, pd.DataFrame):
                create_build_entry(build_df)


class Command(django_subcommands.SubCommands):
    subcommands = {"champion": ChampionStats,
                    "test": Test,
                    }