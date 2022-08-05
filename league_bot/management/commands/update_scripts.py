import django_subcommands

from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.stat_functions.clean_perks_field import separate_perk_fields


class Separate_Perks(BaseCommand):

    def handle(self, *args, **kwargs):
        all_part_rows = Participant.objects.values()
        for part_row in all_part_rows:
            perks, stat = separate_perk_fields(part_row['perks'])
            Participant.objects.filter(id=part_row['id']).update(
                perks=perks,
                stat=stat
            )

        pass

class Command(django_subcommands.SubCommands):
    subcommands = {
                    "separate_perks": Separate_Perks,
                    }