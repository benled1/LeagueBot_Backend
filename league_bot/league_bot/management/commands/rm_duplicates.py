from django.core.management.base import BaseCommand
from requests import delete
from league_bot.models import Match, Participant
import django_subcommands


def remove_duplicates_match_table():
    deleted_match_ids = []
    for row in Match.objects.all().reverse():
        if Match.objects.filter(match=row.match).count() > 1:
            deleted_match_ids.append(row.match)
            row.delete()
    return deleted_match_ids

def remove_duplicates_participant_table():
    deleted_match_ids = []
    for row in Participant.objects.all().reverse():
        if Participant.objects.filter(match=row.match).filter(part_puuid=row.part_puuid).count() > 1:
            deleted_match_ids.append(row.match)
            row.delete()
    return deleted_match_ids
    
class RemoveDuplicates(BaseCommand):
    help="This is the hellow_world command"

    def handle(self, *args, **kwargs):
        deleted_matches_from_match = remove_duplicates_match_table()
        deleted_matches_from_participant = remove_duplicates_participant_table()
        print(f"Deleted Matches: {deleted_matches_from_match}")
        print(f"Deleted Participant Entries for Matches: {deleted_matches_from_participant}")
        pass
class Command(django_subcommands.SubCommands):
    subcommands = {"remove_all": RemoveDuplicates}