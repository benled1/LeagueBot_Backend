from ast import Delete
from ctypes import wintypes
from distutils.command.build import build
from numpy import number
import pandas as pd
import django_subcommands

from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion, Champion_Items, Items
from league_bot.stat_functions.champion import get_winrate, get_play_count, get_item_counts



class Delete_Slot_Data(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        get_item_counts("Annie")
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
            print(f"Updating stats for {champion['champ_name']}")
            all_champ_part_records = Participant.objects.filter(champ_name=champion['champ_name']).values('win')

            winrate = get_winrate(all_champ_part_records)
            Champion.objects.filter(champ_name=champion['champ_name']).update(champ_winrate=winrate)

            play_count = get_play_count(all_champ_part_records=all_champ_part_records)
            Champion.objects.filter(champ_name=champion['champ_name']).update(champ_play_count=play_count)

            try:
                item_counts = get_item_counts(champion_name=champion['champ_name'])
            except KeyError:
                continue
            for index, row in item_counts.iterrows():
                print(f"INDEX:{index}")
                Champion_Items.objects.update_or_create(
                    info_key=row['info_key'],
                    defaults={
                    'info_key':row['info_key'],
                    'champ_name':Champion.objects.get(champ_name=champion['champ_name']),
                    'item_id':Items.objects.get(item_id=index),
                    'play_count':row['counts']
                    }
                )


            """
            For next time:
            update all the fields in Champion_Items Model, all the info is there in item_counts df ^^^
             ALSO ADD THE FIELD 'BUILDS INTO' THIS CAN BE USED TO CHECK IF FULL ITEM OR NOT SINCE 
             FULL ITEMS DO NOT HAVE INTO ANYTHING
            """
            


class Command(django_subcommands.SubCommands):
    subcommands = {"champion": ChampionStats,
                    "delete_slot_data": Delete_Slot_Data,
                    }