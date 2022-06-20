
def get_winrate(all_champ_part_records):
    number_of_records = all_champ_part_records.count()
    number_of_wins = all_champ_part_records.filter(win=1).count()
    if number_of_records == 0:
        return -1
    else:
        winrate = round((number_of_wins/number_of_records), 2)
        return winrate

def get_play_count(all_champ_part_records):
    number_of_records = all_champ_part_records.count()
    return number_of_records