from distutils.command.build import build
import pandas as pd
import requests
import json
import os

from league_bot.models import Participant
from django.db.models import Count, Sum


def get_winrate(all_champ_part_records):
    number_of_records = all_champ_part_records.count()
    number_of_wins = all_champ_part_records.filter(win=1).count()
    if number_of_records == 0:
        return -1
    else:
        winrate = round((number_of_wins/number_of_records), 4)
        return winrate


def get_play_count(all_champ_part_records):
    number_of_records = all_champ_part_records.count()
    return number_of_records


def get_item_counts(champion_name):
    champ_entries = Participant.objects.filter(champ_name=champion_name).values()
    part_df = pd.DataFrame(champ_entries)
    part_df_items = part_df[['item0', 'item1', 'item2', 'item3', 'item4', 'item5']]
    item_counts = part_df_items.apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False).drop(0, axis=0)
    champion_items = pd.DataFrame(item_counts, columns=['counts'])
    champion_items['info_key'] = champion_items.index.astype(str) + str(champion_name)
    print(champion_items)
    return champion_items
    

    # print(f"{len(total_build_counts)} builds for {champion_name}")
    # for build in total_build_counts:
    #     if build not in win_build_counts:
    #         build['build_winrate'] = 0.0
        
    #     win_build_index = win_build_counts
        



