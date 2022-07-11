import requests
import os
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_champion_picture(champ_name):
        response = requests.get(f"{os.getenv(f'DATA_DRAGON_CHAMP_IMAGE_URL')}{champ_name}.png")
        champ_img = Image.open(BytesIO(response.content))
        if champ_name != 'MonkeyKing':
            champ_name = champ_name
        else:
            champ_name = "Wukong"
        champ_img.save(f"league_bot/tmp_images/champ_pics/{champ_name}.png", "PNG")
        return champ_name