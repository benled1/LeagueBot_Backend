import base64
import json
from wsgiref.validate import PartialIteratorWrapper
from league_bot.models import Participant
from ninja import NinjaAPI
from league_bot.models import Champion
from django.core import serializers
from django.http import HttpResponse

api = NinjaAPI()

@api.get("/add")
def add(request, a: int, b:int):
    return {"result": a + b}

@api.get("/champion_stats")
def champion_stats(request, champ_name: str):
    """
    TRY DOING THIS USING AN S3 BUCKET TO STORE ALL THE IMAGES. GENERATE_IMAGES SHOULD OVERWRITE THE IMAGES IN S3 BUCKET
    A CALL TO THIS FUNCTION SHOULD PROVIDE LINKS TO ALL THE IMAGE LOCATIONS SO THEY CAN BE DOWNLOADED TEMPORARILY
    ONTO THE FRONTEND AND SENT TO THE DISCORD CHANNEL AS AN EMBED. 
    """
    # champion_row = Champion.objects.filter(champ_name=champ_name)
    with open(f'/workspace/league_bot/league_bot/final_images/champ_stat_cards/Annie.png', 'rb') as image_file:
        encoded_champ_img = str(base64.b64encode(image_file.read()))
        # json_img = json.dumps([{'image': encoded_champ_img}])
    # champion_row_json = serializers.serialize('json', champion_row)
    return encoded_champ_img





