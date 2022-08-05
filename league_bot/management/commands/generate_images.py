from ctypes import wintypes
from typing import final
from numpy import number
from io import BytesIO
import pandas as pd
import json
import django_subcommands
import requests
import os
import boto3
from datetime import datetime as dt
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# from dotenv import load_dotenv

from league_bot.image_functions.champ_stat_cards import get_champion_stat_card, get_item_build
from league_bot.image_functions.champ_pictures import get_champion_picture, get_item_picture, get_rune_picture
from django.core.management.base import BaseCommand
from league_bot.models import Champion, Runes, Participant
from league_bot.stat_functions.champion import get_item_counts
from league_bot.image_functions.find_runes import find_runes
from league_bot.stat_functions.clean_perks_field import separate_perk_fields






class Test(BaseCommand):
    def handle(self, *args, **kwargs):
        part_row = Participant.objects.filter(id=1).values()[0]
        separate_perk_fields(part_row['perks'])
        pass

class UploadRunePictures(BaseCommand):
    def handle(self, *args, **kwargs):
        if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/rune_pics"):
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot/", "tmp_images/rune_pics")
            os.mkdir(path)
        s3_resource = boto3.resource('s3')
        rune_dicts = Runes.objects.values()
        for rune in rune_dicts:
            rune_id = rune['rune_id']
            rune_id = get_rune_picture(rune_id)

            print(f"Uploading {rune_id}...")
            first_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{rune_id}/{rune_id}.png")
            first_object.upload_file(f"league_bot/tmp_images/rune_pics/{rune_id}.png")

        

        
class UploadItemPictures(BaseCommand):
    def handle(self, *args, **kwargs):
        if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/item_pics"):
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot/", "tmp_images/item_pics")
            os.mkdir(path)

        response  = requests.get(url=os.getenv("DATA_DRAGON_ITEM_URL"))
        item_dict = json.loads(response.content.decode('utf-8'))
        all_items = list(item_dict['data'].keys())
        s3_resource = boto3.resource('s3')
        for item in all_items:
            item_id = get_item_picture(item_id=item)
        
            print(f"Uploading {item_id}...")
            first_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item_id}/{item_id}.png")
            first_object.upload_file(f"league_bot/tmp_images/item_pics/{item_id}.png")
        pass


class UploadChampionPictures(BaseCommand):
    def handle(self, *args, **kwargs):
        if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/champ_pics"):
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
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

        if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/champ_stat_cards"):
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "champ_stat_cards")
            os.mkdir(path)

        todays_date = dt.now(datetime.timezone.utc).strftime(r"%m-%d-%Y")
        all_champ_rows = Champion.objects.filter(champ_play_count__gt=0).values()
        s3_resource = boto3.resource('s3')
        for champ_row in all_champ_rows:
            champ_name = get_champion_stat_card(champ_row=champ_row)

            # print(f"Uploading {champ_name}...")
            # print(todays_date)
            # first_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"champ_stat_cards/{champ_name}/{champ_name}{todays_date}.png")
            # first_object.upload_file(f"league_bot/tmp_images/champ_stat_cards/{champ_name}.png")

                
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
     "upload_champ_pics": UploadChampionPictures,
     "upload_item_pics": UploadItemPictures,
     "upload_rune_pics": UploadRunePictures,
     "test": Test}