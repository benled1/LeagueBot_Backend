from ctypes import wintypes
from typing import final
from numpy import number
from PIL import Image
from io import BytesIO
import pandas as pd
import django_subcommands
import requests
import os

from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion
from league_bot.stat_functions.champion import get_winrate, get_play_count

def get_champion_picture(champ_name):
        response = requests.get(f"{os.getenv(f'DATA_DRAGON_CHAMP_IMAGE_URL')}{champ_name}.png")
        champ_img = Image.open(BytesIO(response.content))
        return champ_img


class ChampionStats(BaseCommand):
    def handle(self, *args, **kwargs):
        backdrop = Image.open("league_bot/final_images/backdrop/league_backdrop.jpeg")
        champ_img = get_champion_picture("Annie")
        backdrop.paste(champ_img)
        backdrop.save("league_bot/final_images/test.png", "PNG")
        pass
        
class Champions(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):
        champ_img = get_champion_picture("Annie")
        champ_img.save("league_bot/final_images/test.png", "PNG")

class Command(django_subcommands.SubCommands):
    subcommands = {"champions": Champions, "champion_stats": ChampionStats}