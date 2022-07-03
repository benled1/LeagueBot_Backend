from ctypes import wintypes
from typing import final
from numpy import number
from io import BytesIO
import pandas as pd
import django_subcommands
import requests
import os
import boto3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion
from league_bot.stat_functions.champion import get_winrate, get_play_count

def get_champion_picture(champ_name):
        response = requests.get(f"{os.getenv(f'DATA_DRAGON_CHAMP_IMAGE_URL')}{champ_name}.png")
        champ_img = Image.open(BytesIO(response.content))
        return champ_img

def get_champion_stat_card(champ_row):
    champ_winrate = round(champ_row['champ_winrate'] * 100, 2)
    champ_play_count = champ_row['champ_play_count']

    stat_card = Image.open("league_bot/final_images/backdrop/league_backdrop.jpeg")

    draw = ImageDraw.Draw(stat_card)
    number_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Regular.ttf", 30)
    label_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Bold.otf", 12)
    # Draw winrate text and number
    draw.text((20, 20),f"{champ_winrate}%",(115,91, 48),font=number_font)
    draw.text((20, 55),f"WINRATE",(115,91, 48),font=label_font)

    # Draw in champ_playcount and text
    draw.text((20, 100),f"{champ_play_count}",(115,91, 48),font=number_font)
    draw.text((20, 135),f"MATCHES",(115,91, 48),font=label_font)

    return stat_card


class ChampionStats(BaseCommand):
    def handle(self, *args, **kwargs):
        all_champ_rows = Champion.objects.values()
        s3_resource = boto3.resource('s3')
        for champ_row in all_champ_rows:
            print(f"Uploading {champ_row['champ_name']}...")
            # champ_card = get_champion_stat_card(champ_row=champ_row)
            first_object = s3_resource.Object(bucket_name="league-bot-images", key=f"champ_stat_pages/{champ_row['champ_name']}/{champ_row['champ_name']}.png")
            first_object.upload_file(f"league_bot/final_images/champ_stat_cards/{champ_row['champ_name']}.png")

            # champ_card.save(f"league_bot/final_images/champ_stat_cards/{champ_row['champ_name']}.png", "PNG")
           
        
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