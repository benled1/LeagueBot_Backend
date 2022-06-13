import requests
import os
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

"""
CURRENTLY DEALING WITH RATE LIMITING ISSUES BY TRYING TO RESPOND TO DIFFERENT
RESPONSE CODES USING IF ELSE.
"""



def get_puuid(summoner_name):
    
    """
    Take a list of summoner names that belong to Challenger League players. This list is retrieved from
    the get_challenger_players() function. Make calls to the players to retrieve the puuids of the players.

    IN THE FUTURE MAKE THIS RETURN ONLY ONE PUUID AND ACCEPT ONLY ONE NAME
    WHEN THIS IS DONE THE RATE LIMITING NEEDS TO BE REFACTORED SLIGHTLY
    :param summoner_name:
    :return:
    """
    limit_calls()
    print(f'Grabbing puuid for {summoner_name}...')
    try:
        quote_summoner = quote(summoner_name)
    except TypeError:
        print(summoner_name)
        raise Exception("Error: In get_puuid(). Quote was expecting bytes and didn't get it.")

    try:
        response = requests.get(
            f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{quote_summoner}",
            headers=header)
    except:
        print("Error: Failed to get puuid. Skipping...")
        return None

    if response.status_code != 200:
        raise Exception(f'Error: Request returned code {response.status_code}')
        print(response.status_code)
        return response.status_code

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
        raise Exception(f'Error: Request returned code {response.status_code}')
        return None

    chall_response = response.content
    chall_dict = json.loads(chall_response)

    chall_entries = chall_dict['entries']
    chall_summoners = []

    for summoner in chall_entries:
        chall_summoners.append(summoner['summonerName'])

    return chall_summoners


