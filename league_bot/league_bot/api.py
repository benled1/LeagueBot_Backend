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
    champion_row = Champion.objects.filter(champ_name=champ_name)
    champion_row_json = serializers.serialize('json', champion_row)
    return champion_row_json




