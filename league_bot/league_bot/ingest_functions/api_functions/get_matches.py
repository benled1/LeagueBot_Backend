from typing import Type
import requests
import os
import ast
import json

from dotenv import load_dotenv
from urllib.parse import quote
from .rate_limiting import limit_calls

load_dotenv()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.getenv('RIOT_KEY')
}



def get_match_history(puuid, length=20):
    """
    Get the match_ids of the last 20 games played by the player with puuid.
    :param puuid: the puuid of the player who played the matches
    :param length: the amount of matches to return in the list
    :return: a list of the match_id's in the players' history.
    """
    limit_calls()
    try:
        quote_puuid = quote(puuid)
    except TypeError:
        print(puuid)
        raise Exception("Error: In get_match_history(). Quote was expecting bytes and didn't get it.")
    try:
        response = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
                                f'{quote_puuid}'
                                f'/ids?start=0&count={length}', headers=header)
    except:
        print("Error: Failed to get match history. Skipping...")
        return None

    if response.status_code != 200:
        print(f'Error: Request returned code {response.status_code}')
        return None

    match_id_list = response.content
    match_id_list = ast.literal_eval(match_id_list.decode('UTF-8'))

    return match_id_list


def get_match_details(match_id):
    """
    get the details of a specific match with match_id.
    :param match_id: the id of the match being detailed.
    :return: a python dictionary containing the match details.
    """
    limit_calls()
    try:
        quote_match_id = quote(match_id)
    except TypeError:
        print(match_id)
        print("Error: In get_match_details. Quote was expecting bytes and didn't get it.")
        return None
    
    try:
        response = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{quote_match_id}',
                            headers=header)
    except:
        print("Error: Failed to get match details. Skipping...")
        return None

    if response.status_code != 200:
        print(f'Error: Request returned code {response.status_code}')
        return None

    match_details = response.content
    match_details = json.loads(match_details)
    if match_details['info']['gameMode'] != "CLASSIC":
        print("Non-Classic game, skipping...")
        return None
    else:
        print("Retrieving match details...")
    return match_details
