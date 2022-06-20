import pandas as pd

from . import construct_tables
from .api_functions import get_summoners, get_matches
from .api_functions import exceptions
from itertools import chain
import warnings


def save_chall_match_tables(all_match_hists):
    """
    Save tables for "amount" number of challenger players.
    :param amount: an integer representing the number of players that will be looped over.
    :return: match_table dataframe
            The match table has a row per match that was played by each player (the matches are found in the player's
            match_history)
    """
    # initial pandas row
    match_table = pd.DataFrame()
    for match_hist_ids in all_match_hists:
        match_table = pd.concat([match_table, construct_tables.get_match_table(match_hist_ids)])
        if match_table is None:
            continue

    # drop the duplicate rows in the match tables since some players play the same games
    match_table.drop_duplicates(keep='first', inplace=True)
    # match_table.to_csv("./csv_files/saved_match_table.csv")
    return match_table


def save_chall_participant_tables(all_match_hists):
    """
    Save tables for "amount" number of challenger players.
    :param amount: an integer representing the number of players that will be looped over.
    :return: participant_table dataframe
            The participant_table is a table of all the participants in each match in the match_table above.
            Each row in the participant table will contain info about the stats of a specific player in a specific
            match.
    """

    # flatten the 2D array
    match_hists = list(chain.from_iterable(all_match_hists))

    # initial pandas df
    participant_table = pd.DataFrame()

    # loop through match_ids and add all the participants from each match as a row in the participant table
    for match_id in match_hists:
        try:
            part_table = construct_tables.get_participant_table(match_id)
        except exceptions.BadResponseGetMatchDetails as exc:
            warnings.warn(f"Failed to get match details for {exc.match_id} with code {exc.status_code}")
            continue
        except exceptions.InvalidMatchType as exc:
            warnings.warn(f"Invalid match type {exc.match_type}, skipping...")
            continue
        participant_table = pd.concat([participant_table, part_table])

    return participant_table

def pre_process(amount):
    print("Collecting Challenger Players...")
    try:
        sum_list = get_summoners.get_challenger_players()
    except exceptions.BadResponseGetChallengers as exc:
        raise exceptions.BadResponseGetChallengers(f"Returned code: {exc.status_code}")
    print("Challenger Players Collected!")

    print("Finding puuids...")
    puuid_list = []
    for summoner in sum_list[0:min(amount, len(sum_list))]:
        try:
            puuid_list.append(get_summoners.get_puuid(summoner))
        except exceptions.BadResponseGetPuuid as exc:
            warnings.warn(f"Failed to get puuid for {exc.player_name} with code: {exc.status_code}")
            continue
        except exceptions.PlayerQuoteFailed as exc:
            warnings.warn(f"Failed to quote {exc.summoner_name}")
            continue

    print("Puuids found!")

    all_match_hists = []
    for puuid in puuid_list:
        try:
            match_hist_ids = get_matches.get_match_history(puuid=puuid, length=20)
        except exceptions.BadResponseGetMatchHistory as exc:
            warnings.warn(f"Failed to get match history for {exc.puuid} with code: {exc.status_code}")
            continue
        except exceptions.PuuidQuoteFailed as exc:
            warnings.warn(f"Failed to quote {exc.puuid}")
            continue
        all_match_hists.append(match_hist_ids)

    return all_match_hists

def ingest_tables(amount=20):
    
    all_match_hists = pre_process(amount)
    
    print("Saving Match Tables...")
    match_table = save_chall_match_tables(all_match_hists)
    print("Match Tables Complete!")

    print("Saving Participant Tables...")
    participant_table = save_chall_participant_tables(all_match_hists)
    participant_table.drop_duplicates(subset=['summonerName', 'match_id'], keep='first', inplace=True)
    print("Participant Tables Complete!")


    return match_table, participant_table