from distutils.command.build import build
import pandas as pd

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


def get_best_builds(champion_name):
    win_build_counts = (Participant.objects
    .filter(champ_name=champion_name)
    .filter(win=True)
    .values('champ_name', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5')
    .annotate(build_count=Count("id"))
    .order_by("-build_count"))

    total_build_counts = (Participant.objects
    .filter(champ_name=champion_name)
    .values('champ_name', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5')
    .annotate(build_count=Count("id"))
    .order_by("-build_count"))

    total_df = pd.DataFrame(total_build_counts)
    win_df = pd.DataFrame(win_build_counts)
    if len(total_df) != 0:
        build_df = pd.merge(
                total_df, win_df,  how='left',
                left_on=['champ_name', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5'],
                right_on = ['champ_name', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5']
                )
        build_df.rename(columns={'build_count_x': 'num_plays',
                                'build_count_y': 'num_wins'}, inplace=True)
        build_df.fillna(value=0.0, inplace=True)
        build_df['win_rate'] = build_df['num_wins']/build_df['num_plays']
        build_df['build_id'] = build_df['item0'].astype(str) + \
                            build_df['item1'].astype(str) + \
                            build_df['item2'].astype(str) + \
                            build_df['item3'].astype(str) + \
                            build_df['item4'].astype(str) + \
                            build_df['item5'].astype(str)
                                
        build_df.sort_values(by='win_rate', ascending=False, inplace=True)
    else:
        return "No Builds"
    return build_df

    # print(f"{len(total_build_counts)} builds for {champion_name}")
    # for build in total_build_counts:
    #     if build not in win_build_counts:
    #         build['build_winrate'] = 0.0
        
    #     win_build_index = win_build_counts
        



