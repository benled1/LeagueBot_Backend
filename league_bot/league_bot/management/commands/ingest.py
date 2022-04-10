from django.core.management.base import BaseCommand
from league_bot.models import Test
from league_bot.ingest_functions.save_tables import ingest_tables
import django_subcommands

class Challengers(BaseCommand):
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        match_table, part_table = ingest_tables(amount=3)
        self.stdout.write(f"{match_table}")
        pass

class Command(django_subcommands.SubCommands):
    subcommands = {"challengers": Challengers}

