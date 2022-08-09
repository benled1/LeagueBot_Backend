import pandas as pd
import django_subcommands
import json
import requests
import os

from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from django.db.utils import IntegrityError
from league_bot.models import Match, Participant, Champion, Items, Runes
# from league_bot.stat_functions import champ_group

def get_rune_dict():
    response = requests.get(os.getenv('DATA_DRAGON_RUNE_URL'))
    rune_dict = json.loads(response.content)
    print(type(rune_dict))
    return rune_dict


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
            try:
                item_text = item_dict[item]['description']
            except KeyError:
                item_text = ""
            Items.objects.update_or_create(
                item_id=item,
                defaults={
                'item_id':item,
                'item_name':item_dict[item]['name'],
                'gold':item_dict[item]['gold']['total'],
                'tags':item_dict[item]['tags'],
                'builds_into':into,
                'description':item_text
                }
                )

        print(item_dict)

class Ingest_Runes(BaseCommand):
    def handle(self, *args, **kwargs):
        Runes.objects.all().delete()
        rune_dict = get_rune_dict()

        for rune in rune_dict:
            Runes.objects.update_or_create(
                rune_id=rune['id'],
                defaults={
                'rune_id':rune['id'],
                'rune_name':rune['name'],
                'rune_icon':rune['icon']
                }
            )
        for index in range(len(rune_dict)):
            for rune_dicts_list in rune_dict[index]['slots']:
                for rune in rune_dicts_list['runes']:
                    Runes.objects.update_or_create(
                        rune_id=rune['id'],
                        defaults={
                        'rune_id':rune['id'],
                        'rune_name':rune['name'],
                        'rune_icon':rune['icon']
                        }
                    )

        

class Test(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        champ_name_list = get_champ_dict()
        for name in champ_name_list:
            Champion.objects.update_or_create(
                champ_name = name,
                defaults={'champ_name' : name})


class Command(django_subcommands.SubCommands):
    subcommands = {"test": Test,
                    "items": Ingest_Items,
                    "runes": Ingest_Runes}