from league_bot.models import Participant
from django.db.models import Count

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
    best_build_query_set = (Participant.objects
    .values('item0', 'item1', 'item2', 'item3', 'item4', 'item5')
    .annotate(build_count=Count("id"))
    .order_by("-build_count"))
    print(best_build_query_set)