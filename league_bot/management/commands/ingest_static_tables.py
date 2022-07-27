import pandas as pd
import django_subcommands
import json
import requests
import os

from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from django.db.utils import IntegrityError
from league_bot.models import Match, Participant, Champion, Items
# from league_bot.stat_functions import champ_group


def get_champ_dict():
    response = requests.get(os.getenv('DATA_DRAGON_CHAMP_URL'))
    champ_dict = json.loads(response.content)
    champ_name_list = list(champ_dict['data'].keys())
    return champ_name_list    

def get_item_dict():
    response = requests.get(os.getenv('DATA_DRAGON_ITEM_URL'))
    item_dict = json.loads(response.content)
    return item_dict['data']


class Ingest_Items(BaseCommand):
    def handle(self, *args, **kwargs):
        item_dict = get_item_dict()
        Items.objects.all().delete()
        for item in list(item_dict.keys()):
            try:
                into = item_dict[item]['into']
            except KeyError:
                into = []
            Items.objects.update_or_create(
                item_id=item,
                item_name=item_dict[item]['name'],
                gold=item_dict[item]['gold']['total'],
                tags=item_dict[item]['tags'],
                builds_into=into)
        print(item_dict)

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
    subcommands = {"test": Test,
                    "items": Ingest_Items}