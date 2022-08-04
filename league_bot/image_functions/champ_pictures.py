import requests
import os
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from league_bot.models import Runes


def get_champion_picture(champ_name):
        response = requests.get(f"{os.getenv(f'DATA_DRAGON_CHAMP_IMAGE_URL')}{champ_name}.png")
        champ_img = Image.open(BytesIO(response.content))
        if champ_name != 'MonkeyKing':
            champ_name = champ_name
        else:
            champ_name = "Wukong"
        champ_img.save(f"league_bot/tmp_images/champ_pics/{champ_name}.png", "PNG")
        return champ_name

def get_item_picture(item_id):
        response = requests.get(f"{os.getenv(f'DATA_DRAGON_ITEM_IMAGE_URL')}{item_id}.png")
        champ_img = Image.open(BytesIO(response.content))
        champ_img.save(f"league_bot/tmp_images/item_pics/{item_id}.png", "PNG")
        return item_id

def get_rune_picture(rune_id):
    rune_row = Runes.objects.filter(rune_id=rune_id).values()[0]
    rune_cat = rune_row['rune_cat']
    rune_name = rune_row['rune_name']
    response = requests.get(f"{os.getenv(f'DATA_DRAGON_RUNE_IMAGE_URL')}{rune_cat}/{rune_name}/{rune_name}.png")
    if response.status_code == 200:
        champ_img = Image.open(BytesIO(response.content))
        
        champ_img.save(f"league_bot/tmp_images/rune_pics/{rune_name}.png", "PNG")
    else:
        # print(response.status_code)
        # print(response.content)
        # print(rune_row['rune_name'])
        pass