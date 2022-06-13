from league_bot.models import Participant, Match

def champ_winrate():
    part_table = Participant.objects.values_list()
    print(part_table)
    pass