from ctypes import wintypes
from typing import final
from numpy import number
from io import BytesIO
import pandas as pd
import django_subcommands
import requests
import os
import boto3
from datetime import datetime as dt
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from league_bot.image_functions.champ_stat_cards import get_champion_stat_card
from league_bot.image_functions.champ_pictures import get_champion_picture
from league_bot.models import Participant
from django.core.management.base import BaseCommand
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Champion
from league_bot.stat_functions.champion import get_winrate, get_play_count


class UploadChampionPictures(BaseCommand):
    def handle(self, *args, **kwargs):
        if not os.path.isdir("league_bot/tmp_images/champ_stat_cards"):
            path = os.path.join("app/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "champ_pics")
            os.mkdir(path)


        all_champ_rows = Champion.objects.values()
        s3_resource = boto3.resource('s3')
        for champ_row in all_champ_rows:
            champ_name = get_champion_picture(champ_row['champ_name'])
        
            print(f"Uploading {champ_name}...")
            first_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"champ_pics/{champ_name}/{champ_name}.png")
            first_object.upload_file(f"league_bot/tmp_images/champ_pics/{champ_name}.png")


class UploadChampionStatCards(BaseCommand):
    def handle(self, *args, **kwargs):

        if not os.path.isdir("league_bot/tmp_images/champ_stat_cards"):
            path = os.path.join("app/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "champ_stat_cards")
            os.mkdir(path)

        todays_date = dt.now(datetime.timezone.utc).strftime(r"%m-%d-%Y")
        all_champ_rows = Champion.objects.values()
        s3_resource = boto3.resource('s3')
        for champ_row in all_champ_rows:
            champ_name = get_champion_stat_card(champ_row=champ_row)

            print(f"Uploading {champ_name}...")
            print(todays_date)
            first_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"champ_stat_cards/{champ_name}/{champ_name}{todays_date}.png")
            first_object.upload_file(f"league_bot/tmp_images/champ_stat_cards/{champ_name}.png")

                
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
    subcommands = {"champions": Champions,
     "upload_champ_stat_cards": UploadChampionStatCards,
     "upload_champ_pics": UploadChampionPictures}