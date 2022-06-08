import requests
import os
import json

from urllib.parse import quote
from ratelimit import limits, sleep_and_retry


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


@sleep_and_retry
@limits(calls=90, period=120)
def get_puuid(summoner_name):
    
    """
    Take a list of summoner names that belong to Challenger League players. This list is retrieved from
    the get_challenger_players() function. Make calls to the players to retrieve the puuids of the players.

    IN THE FUTURE MAKE THIS RETURN ONLY ONE PUUID AND ACCEPT ONLY ONE NAME
    WHEN THIS IS DONE THE RATE LIMITING NEEDS TO BE REFACTORED SLIGHTLY
    :param summoner_name:
    :return:
    """
    response = requests.get(
        f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{quote(summoner_name)}",
        headers=header)


    if response.status_code != 200:
        print(response.status_code)
        return None

    content = response.content
    summoner_dict = json.loads(content)

    puuid = summoner_dict['puuid']
    # print(f"PUUID: {summoner_name} {type(puuid)}")
    return puuid


@sleep_and_retry
@limits(calls=90, period=120)
def get_challenger_players():
    """
    get a list of all challenger players names in league fo legends
    :return:
    """
    response = requests.get(
                            "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5",
                            headers=header)

    if response.status_code != 200:
        return None

    chall_response = response.content
    chall_dict = json.loads(chall_response)

    chall_entries = chall_dict['entries']
    chall_summoners = []

    for summoner in chall_entries:
        chall_summoners.append(summoner['summonerName'])

    # print(f"Challenger Players: {type(chall_summoners)}")

    return chall_summoners


