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
    # champion_row = Champion.objects.filter(champ_name=champ_name)
    with open(f'/Users/benledingham/Documents/League Bot/League_App/league_bot/league_bot/final_images/champ_stat_cards/Annie.png', 'rb') as imageFile:
        encoded_champ_img = base64.b64encode(imageFile.read()).decode('utf-8')
    json_img = json.dumps([{'image': encoded_champ_img}])
    # champion_row_json = serializers.serialize('json', champion_row)
    return json_img





