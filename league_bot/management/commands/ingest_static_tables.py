import pandas as pd
import django_subcommands
import json
import requests
import os

from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from django.db.utils import IntegrityError
from league_bot.models import Match, Participant, Champion
# from league_bot.stat_functions import champ_group


def get_champ_dict():
    response = requests.get(os.getenv('DATA_DRAGON_CHAMP_URL'))
    champ_dict = json.loads(response.content)
    champ_name_list = list(champ_dict['data'].keys())
    return champ_name_list    


class Test(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        champ_name_list = get_champ_dict()
        for name in champ_name_list:
            Champion.objects.update_or_create(champ_name = name)
            
        



class Command(django_subcommands.SubCommands):
    subcommands = {"test": Test}