from distutils.command.build import build

import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from dotenv import load_dotenv
from .find_build import get_item_build
from .add_pictures import add_items, add_winrate_playcount, add_runes
from .find_runes import get_rune_build
from league_bot.models import Champion_Items, Champion, Items
from django.db.models import Q

load_dotenv()
"""
For next time:

Continue working on adding the item images to the champ_stat_card:

- This will require that you download and save the images from s3 to
    a tmp folder. These tmp folders are destroyed when the dyno is re-run since they are 
    ignored in the git folder.
- Once the images are downloaded and stored in tmp folder, load them into PIL and 
    overlay them on the champ_stat_card how you want

"""

def get_champion_stat_card(champ_row):
    champ_winrate = round(champ_row['champ_winrate'] * 100, 2)
    champ_play_count = champ_row['champ_play_count']

    stat_card = Image.open("league_bot/static_images/backdrop.jpeg")
    stat_card = add_winrate_playcount(stat_card=stat_card, champ_winrate=champ_winrate, champ_play_count=champ_play_count)

    
    if champ_row['champ_name'] != 'MonkeyKing':
        front_facing_champ_name = champ_row['champ_name']
        print(f"Adding build for {front_facing_champ_name}")
        build_dict = get_item_build(champ_name=front_facing_champ_name)
        add_items(build_dict=build_dict, stat_card=stat_card)
        rune_dict = get_rune_build(champ_name=front_facing_champ_name)
        add_runes(rune_dict=rune_dict, stat_card=stat_card)
    else:
        champ_name = champ_row['champ_name']
        print(f"Adding build for {champ_name}")
        build_dict = get_item_build(champ_name=champ_name)
        add_items(build_dict=build_dict, stat_card=stat_card)
        rune_dict = get_rune_build(champ_name=champ_name)
        front_facing_champ_name = "Wukong"
    stat_card.save(f"league_bot/tmp_images/champ_stat_cards/{front_facing_champ_name}.png", "PNG")

    return front_facing_champ_name

