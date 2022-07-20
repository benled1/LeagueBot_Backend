import requests
import os
import json

from .exceptions import PlayerQuoteFailed, BadResponseGetChallengers, BadResponseGetPuuid
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

def get_puuid(summoner_name):
    
    """
    Take a list of summoner names that belong to Challenger League players. This list is retrieved from
    the get_challenger_players() function. Make calls to the players to retrieve the puuids of the players.

    :param summoner_name:
    :return:
    """
    limit_calls()

    print(f'Grabbing puuid for {summoner_name}...')
    try:
        quote_summoner = quote(summoner_name)
    except TypeError:
        raise PlayerQuoteFailed(summoner_name=summoner_name)


    response = requests.get(
        f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{quote_summoner}",
        headers=header)

    if response.status_code != 200:
        raise BadResponseGetPuuid(code=response.status_code, player_name=summoner_name)

    content = response.content
    summoner_dict = json.loads(content)

    puuid = summoner_dict['puuid']
    return puuid


def get_challenger_players():
    """
    get a list of all challenger players names in league fo legends
    :return:
    """
    limit_calls()

    response = requests.get(
                            "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
                            headers=header)

    
    if response.status_code != 200:
        raise BadResponseGetChallengers(code=response.status_code)

    chall_response = response.content
    chall_dict = json.loads(chall_response)

    chall_entries = chall_dict['entries']
    chall_summoners = []

    for summoner in chall_entries:
        chall_summoners.append(summoner['summonerName'])

    return chall_summoners


