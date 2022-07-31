from distutils.command.build import build
from turtle import xcor, ycor
import boto3
import os
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from dotenv import load_dotenv
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


def add_winrate_playcount(stat_card, champ_winrate, champ_play_count):
    """
    :param stat_card: The PIL object to be drawn onto
    :param champ_winrate: The winrate of the champion 
    :param champ_play_count: The number of games the champion has been recorded playing. 
    """
    draw = ImageDraw.Draw(stat_card)
    number_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Regular.ttf", 100)
    label_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Bold.otf", 25)
    # Draw winrate text and number
    draw.text((20, 20),f"{champ_winrate}%",(115,91, 48),font=number_font)
    draw.text((70, 120),f"WINRATE",(115,91, 48),font=label_font)

    # Draw in champ_playcount and text
    draw.text((20, 300),f"{champ_play_count}",(115,91, 48),font=number_font)
    draw.text((20, 400),f"MATCHES",(115,91, 48),font=label_font)
    return stat_card

def find_best_boots(champ_name):
    all_boots = list(Items.objects.filter(tags__contains=["Boots"]).values())
    all_boot_ids = [item_dict['item_id'] for item_dict in all_boots]

  
    champion_boots = list(Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_boot_ids).order_by("-play_count").values())
    if champion_boots != []:
        best_boots = champion_boots[0]
        return best_boots
    
    return "no_boots"

def find_best_mythic(champ_name):
    all_mythics = list(Items.objects.filter(description__contains="rarityMythic").values())
    all_mythic_ids = [item_dict['item_id'] for item_dict in all_mythics]


    champion_mythic = Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_mythic_ids).order_by("-play_count").values()
    best_mythic = champion_mythic[0]
    return best_mythic

def find_best_full_items(champ_name, count=4):
    all_full_items = list(Items.objects.filter(builds_into=[]).filter(gold__gte=500).values().filter(~Q(tags__contains=["Boots"])))
    all_full_item_ids = [item_dict['item_id'] for item_dict in all_full_items]

    champion_full_items = list(Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_full_item_ids).order_by("-play_count").values())
    best_full_items = champion_full_items[:count]
    return best_full_items
    

def get_item_build(champ_name):
    """
    TODO:
    - Finish the find best boots function
    - Finish the find mythic function (take into consideration that Ornn items have different item ids as
        the regular mythic even though same item.)
    - Finish finding remaining full items function
    - NOTE: Mythic items say mythic in the plaintext field, try adding that to model,
    - NOTE: Ornn upgrades have reuired_Ally: Ornn in dict, add that to model too
    - NOTE: do some check to see if Ornn item and then match it to the actual item.
    - NOTE: If all else fails, just hardcode a dict or smth >:)
    """
    best_boots = find_best_boots(champ_name=champ_name)
    best_mythic = find_best_mythic(champ_name=champ_name)
    if best_boots == "no_boots":
        best_full_items = find_best_full_items(champ_name=champ_name, count=5)
        best_build_dict = {
        "boots/item5": best_full_items[4],
        "mythic": best_mythic,
        "item1": best_full_items[0],
        "item2": best_full_items[1],
        "item3": best_full_items[2],
        "item4": best_full_items[3],
    }
    else:
        best_full_items = find_best_full_items(champ_name=champ_name)
        best_build_dict = {
        "boots/item5": best_boots,
        "mythic": best_mythic,
        "item1": best_full_items[0],
        "item2": best_full_items[1],
        "item3": best_full_items[2],
        "item4": best_full_items[3],
    }

    
    return best_build_dict

def add_items(build_dict, stat_card):

    if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/item_pics"):
        try:
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "item_pics")
            os.mkdir(path)
        except FileExistsError:
            path = os.path.join(path, "item_pics")
            os.mkdir(path)

    s3_resource = boto3.resource('s3')
    print(build_dict['boots/item5']['item_id_id'])
    boots_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['boots/item5']['item_id_id']}/{build_dict['boots/item5']['item_id_id']}.png")
    boots_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['boots/item5']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['boots/item5']['item_id_id']}.png")
    x_pos, y_pos = (400,100)
    stat_card.paste(item, (x_pos, y_pos))

    mystic_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['mythic']['item_id_id']}/{build_dict['mythic']['item_id_id']}.png")
    mystic_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['mythic']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['mythic']['item_id_id']}.png")
    x_pos, y_pos = (500,100)
    stat_card.paste(item, (x_pos, y_pos))


    pass
    

def get_champion_stat_card(champ_row):
    champ_winrate = round(champ_row['champ_winrate'] * 100, 2)
    champ_play_count = champ_row['champ_play_count']

    stat_card = Image.open("league_bot/static_images/backdrop.jpeg")
    stat_card = add_winrate_playcount(stat_card=stat_card, champ_winrate=champ_winrate, champ_play_count=champ_play_count)

    
    if champ_row['champ_name'] != 'MonkeyKing':
        champ_name = champ_row['champ_name']
        print(f"Adding build for {champ_name}")
        build_dict = get_item_build(champ_name=champ_name)
        add_items(build_dict=build_dict, stat_card=stat_card)
    else:
        champ_name = champ_row['champ_name']
        print(f"Adding build for {champ_name}")
        build_dict = get_item_build(champ_name=champ_name)
        add_items(build_dict=build_dict, stat_card=stat_card)
        champ_name = "Wukong"
    stat_card.save(f"league_bot/tmp_images/champ_stat_cards/{champ_name}.png", "PNG")

    return champ_name

