import pandas as pd

from . import construct_tables
from .api_functions import get_summoners, get_matches
from itertools import chain


def save_chall_match_tables(sum_list, amount=20):
    """
    Save tables for "amount" number of challenger players.
    :param amount: an integer representing the number of players that will be looped over.
    :return: multiple dataframes (match_table, participant_table)
            The match table has a row per match that was played by each player (the matches are found in the player's
            match_history)
            The participant_table is a table of all the participants in each match in the match_table above.
            Each row in the participant table will contain info about the stats of a specific player in a specific
            match.
    """
    # initial pandas row
    match_table = pd.DataFrame()

    for summoner in sum_list[0:min(amount, len(sum_list))]:
        match_table = pd.concat([match_table, construct_tables.get_match_table(summoner)])
        if match_table is None:
            continue

    # drop the duplicate rows in the match tables since some players play the same games
    match_table.drop_duplicates(keep='first', inplace=True)
    # match_table.to_csv("./csv_files/saved_match_table.csv")
    return match_table


def save_chall_participant_tables(sum_list, amount=20):

    match_hists = []
    for summoner in sum_list[0:min(amount, len(sum_list))]:
        puuid = get_summoners.get_puuid(summoner)
        match_hists.append(get_matches.get_match_history(puuid))

    # THIS IS WHAT IS CAUSING THE UNICODE ERROR
    # flatten the 2D array
    match_hists = list(chain.from_iterable(match_hists))


    # initial pandas df
    participant_table = pd.DataFrame()
    # loop through match_ids and add all the participants from each match as a row in the participant table
    for match_id in match_hists:
        participant_table = pd.concat([participant_table, construct_tables.get_participant_table(match_id)])
        if participant_table is None:
            return None

    # drop the duplicate rows in the participant tables since some players play the same games
    # participant_table.drop_duplicates(keep='first', inplace=True)
    # participant_table.to_csv("./csv_files/saved_participant_table.csv")
    return participant_table

def ingest_tables(amount=20):
    
     # get a list of summoner names that are in challenger
    sum_list = get_summoners.get_challenger_players()
    if sum_list is None:
        raise Exception('Failed to retrieve Challenger Players')

    match_table = save_chall_match_tables(sum_list, amount)
    participant_table = save_chall_participant_tables(sum_list, amount)

    return match_table, participant_table