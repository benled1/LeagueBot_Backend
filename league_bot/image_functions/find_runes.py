from league_bot.models import Participant
from django.db.models import Count

def find_runes(champ_name):
    champ_counts = Participant.objects.filter(champ_name=champ_name).values('perks').annotate(perk_counts=Count('perks')).order_by("-perk_counts")
    print(champ_counts)
    pass