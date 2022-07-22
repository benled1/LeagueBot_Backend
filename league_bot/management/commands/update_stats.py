from ast import Delete
from ctypes import wintypes
from distutils.command.build import build
from numpy import number
import pandas as pd
import django_subcommands

from league_bot.models import Participant, Slot_0_Items, Slot_1_Items, Slot_2_Items, Slot_3_Items, Slot_4_Items, Slot_5_Items
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion
from league_bot.stat_functions.champion import get_bis_item, get_winrate, get_play_count


def create_item_entry(input_df, slot_num):
    
    for index, row in input_df.iterrows():
        if slot_num == 0:
            Slot_0_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item0 = row['item0'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )
        elif slot_num == 1:
            Slot_1_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item1 = row['item1'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )
        elif slot_num == 2:
            Slot_2_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item2 = row['item2'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )
        elif slot_num == 3:
            Slot_3_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item3 = row['item3'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )
        elif slot_num == 4:
            Slot_4_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item4 = row['item4'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )
        elif slot_num == 5:
            Slot_5_Items.objects.create(
                build_id = row['item_choice_id'],
                champ_name = Champion.objects.get(champ_name = row['champ_name']),
                item5 = row['item5'],
                play_count = row['num_plays'],
                win_rate = row['win_rate']
            )


class Delete_Slot_Data(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        Slot_0_Items.objects.all().delete()
        Slot_1_Items.objects.all().delete()
        Slot_2_Items.objects.all().delete()
        Slot_3_Items.objects.all().delete()
        Slot_4_Items.objects.all().delete()
        Slot_5_Items.objects.all().delete()
        result = get_bis_item("Akali", slot_num=0)
        print(result)
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

            for slot_num in range(0,6):
                build_df = get_bis_item(champion_name=champion['champ_name'], slot_num=slot_num)
                if isinstance(build_df, pd.DataFrame):
                    create_item_entry(build_df, slot_num=slot_num)


class Command(django_subcommands.SubCommands):
    subcommands = {"champion": ChampionStats,
                    "delete_slot_data": Delete_Slot_Data,
                    }