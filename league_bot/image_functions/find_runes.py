from league_bot.models import Participant
from django.db.models import Count

def get_rune_build(champ_name):
    champ_counts = Participant.objects.filter(champ_name=champ_name).values('perks').annotate(perk_counts=Count('perks')).order_by("-perk_counts")
    best_rune_build = champ_counts[0]
    return best_rune_build