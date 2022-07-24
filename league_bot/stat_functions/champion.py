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


def get_bis_item(champion_name, slot_num):
    """
    Notes on how to build the Slot_N_Item Tables:
    Start by refactoring this code here so that instead of making a pandas dataframe for all the items
    there will be 6 separate pandas dataframes for each item slot. This means changing the .values() so that they only contain a single item slot
    and then changing build_id to item_champ_id and make it the primary key item_id+champ_name.
    Once that is done change the models.py so that instead of builds we have a table for each item slot which contains
    item_champ_id, champ_name, item_id, pick_rate, win_rate.
    Once that is done changing the update_stats function so that it creates 6 separate table inserts into each table depenfding on the slot.
    """
    win_build_counts = (Participant.objects
    .filter(champ_name=champion_name)
    .filter(win=True)
    .values('champ_name', f'item{slot_num}')
    .annotate(build_count=Count("id"))
    .order_by("-build_count"))

    total_build_counts = (Participant.objects
    .filter(champ_name=champion_name)
    .values('champ_name', f'item{slot_num}')
    .annotate(build_count=Count("id"))
    .order_by("-build_count"))

    total_df = pd.DataFrame(total_build_counts)
    win_df = pd.DataFrame(win_build_counts)
    if len(total_df) != 0:
        build_df = pd.merge(
                total_df, win_df,  how='left',
                left_on=['champ_name', f'item{slot_num}'],
                right_on = ['champ_name', f'item{slot_num}']
                )
        build_df.rename(columns={'build_count_x': 'num_plays',
                                'build_count_y': 'num_wins'}, inplace=True)
        build_df.fillna(value=0.0, inplace=True)
        build_df['win_rate'] = build_df['num_wins']/build_df['num_plays']
        build_df['item_choice_id'] = build_df['champ_name'].astype(str) + build_df[f'item{slot_num}'].astype(str)
                                
        build_df.sort_values(by='win_rate', ascending=False, inplace=True)
    else:
        return "No Builds"
    return build_df

    # print(f"{len(total_build_counts)} builds for {champion_name}")
    # for build in total_build_counts:
    #     if build not in win_build_counts:
    #         build['build_winrate'] = 0.0
        
    #     win_build_index = win_build_counts
        



