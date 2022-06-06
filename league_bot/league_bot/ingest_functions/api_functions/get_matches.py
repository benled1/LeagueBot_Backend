import requests
import os
import ast
import json

from urllib.parse import quote
from ratelimit import limits, sleep_and_retry


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": os.environ['RIOT_KEY']
}


@sleep_and_retry
@limits(calls=80, period=120)
def get_match_history(puuid, length=20):
    """
    Get the match_ids of the last 20 games played by the player with puuid.
    :param puuid: the puuid of the player who played the matches
    :param length: the amount of matches to return in the list
    :return: a list of the match_id's in the players' history.
    """
    response = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
                            f'{quote(puuid)}'
                            f'/ids?start=0&count={length}', headers=header)

    if response.status_code != 200:
        return None

    match_id_list = response.content
    match_id_list = ast.literal_eval(match_id_list.decode('UTF-8'))

    # print(f"Match History: {puuid} {type(match_id_list)}")

    return match_id_list


@sleep_and_retry
@limits(calls=80, period=120)
def get_match_details(match_id):
    """
    get the details of a specific match with match_id.
    :param match_id: the id of the match being detailed.
    :return: a python dictionary containing the match details.
    """
    response = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{quote(match_id)}',
                            headers=header)

    if response.status_code != 200:
        print(response.status_code)
        return None

    match_details = response.content
    # print(type(match_details))
    match_details = json.loads(match_details)
    if match_details['info']['gameMode'] != "CLASSIC":
        print("NON-CLASSIC GAME")
        return None

    # print(f"Match Details: {match_id} {type(match_details)}")

    return match_details
