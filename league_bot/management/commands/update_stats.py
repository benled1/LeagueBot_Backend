from ctypes import wintypes
from numpy import number
import pandas as pd
import django_subcommands

from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion
from league_bot.stat_functions.champion import get_winrate, get_play_count, get_best_builds


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



class Command(django_subcommands.SubCommands):
    subcommands = {"champion": ChampionStats,
                    "test": Test,
                    }