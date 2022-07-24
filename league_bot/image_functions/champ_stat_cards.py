from turtle import xcor, ycor
import boto3
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from league_bot.models import Slot_0_Items, Slot_1_Items, Slot_2_Items, Slot_3_Items, Slot_4_Items, Slot_5_Items
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


def get_item_build(champ_name):
    if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/item_pics"):
        path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
        os.mkdir(path)
        path = os.path.join(path, "item_pics")
        os.mkdir(path)

    s3_resource = boto3.resource('s3')
    item_dict = {"slot_0": [], "slot_1": [],
                "slot_2": [], "slot_3": [],
                "slot_4": [], "slot_5": []}
    
    slot_0_items = Slot_0_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_0_items[:3]:
        print(f"{item.item0}.png")
        item_dict["slot_0"].append(item.item0)
        if item.item0 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item0}/{item.item0}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item0}.png")

    slot_1_items = Slot_1_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_1_items[:3]:
        print(f"{item.item1}.png")
        item_dict["slot_1"].append(item.item1)
        if item.item1 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item1}/{item.item1}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item1}.png")

    slot_2_items = Slot_2_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_2_items[:3]:
        print(f"{item.item2}.png")
        item_dict["slot_2"].append(item.item2)
        if item.item2 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item2}/{item.item2}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item2}.png")
    
    slot_3_items = Slot_3_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_3_items[:3]:
        print(f"{item.item3}.png")
        item_dict["slot_3"].append(item.item3)
        if item.item3 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item3}/{item.item3}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item3}.png")

    slot_4_items = Slot_4_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_4_items[:3]:
        print(f"{item.item4}.png")
        item_dict["slot_4"].append(item.item4)
        if item.item4 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item4}/{item.item4}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item4}.png")

    slot_5_items = Slot_5_Items.objects.filter(champ_name=champ_name).order_by("-play_count")
    for item in slot_5_items[:3]:
        print(f"{item.item5}.png")
        item_dict["slot_5"].append(item.item5)
        if item.item5 != 0:
            item_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{item.item5}/{item.item5}.png")
            item_object.download_file(f"league_bot/tmp_images/item_pics/{item.item5}.png")

    return item_dict

def add_items(stat_card, item_dict):
    x_pos = 400
    y_pos = 100
    for curr_item in item_dict["slot_0"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75

    x_pos = 500
    y_pos = 100
    for curr_item in item_dict["slot_1"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75

    x_pos = 600
    y_pos = 100
    for curr_item in item_dict["slot_2"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75

    x_pos = 700
    y_pos = 100
    for curr_item in item_dict["slot_3"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75

    x_pos = 800
    y_pos = 100
    for curr_item in item_dict["slot_4"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75

    x_pos = 900
    y_pos = 100
    for curr_item in item_dict["slot_5"]:
        if curr_item == 0:
            continue
        item = Image.open(f"league_bot/tmp_images/item_pics/{curr_item}.png")
        stat_card.paste(item, (x_pos, y_pos))
        y_pos += 75
    return stat_card


def get_champion_stat_card(champ_row):
    champ_winrate = round(champ_row['champ_winrate'] * 100, 2)
    champ_play_count = champ_row['champ_play_count']

    s3_resource = boto3.resource('s3')

    stat_card = Image.open("league_bot/static_images/backdrop.jpeg")
    stat_card = add_winrate_playcount(stat_card=stat_card, champ_winrate=champ_winrate, champ_play_count=champ_play_count)

    
    if champ_row['champ_name'] != 'MonkeyKing':
        champ_name = champ_row['champ_name']
        item_dict = get_item_build(champ_name=champ_name)
        stat_card = add_items(stat_card=stat_card, item_dict=item_dict)
    else:
        champ_name = "Wukong"
        item_dict = get_item_build(champ_name=champ_name)
        stat_card = add_items(stat_card=stat_card, item_dict=item_dict)
    stat_card.save(f"league_bot/tmp_images/champ_stat_cards/{champ_name}.png", "PNG")

    return champ_name

