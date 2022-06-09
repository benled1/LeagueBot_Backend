import pandas as pd

from . import construct_tables
from .api_functions import get_summoners, get_matches
from itertools import chain

##### THIS IS HOW WE WILL SEND ERRORS THROOUGH THE FUCNTIONS
# PUT ALL THE FUNCTIONS IN THE DIAGRAM INSIDE TRY EXCEPT STATEMENTS AND HAVE A FAILED VARIABLE 
# ONLY RUN THE FUNCTIONS THAT ARE RELIANT ON THE CURRENT FUNCTION IF THE FIALED REMAINS FALSE
# TURN THE FAIL TO TRUE IF CURRENT FUNCTION FAILS
# THIS WILL SKIP TO END OF THIS SINGLE MATCH AND THEREFORE MOVING TO NEXT ONE
"""
EX of the above is

try:
    func1()
except:
    Failed = True

if Failed != True
    try:
        func2()
    except:
        Failed = True

etc....

"""


def save_chall_match_tables(puuid_list):
    """
    Save tables for "amount" number of challenger players.
    :param amount: an integer representing the number of players that will be looped over.
    :return: match_table dataframe
            The match table has a row per match that was played by each player (the matches are found in the player's
            match_history)
    """
    # initial pandas row
    match_table = pd.DataFrame()

    for puuid in puuid_list:
        match_table = pd.concat([match_table, construct_tables.get_match_table(puuid)])
        if match_table is None:
            continue

    # drop the duplicate rows in the match tables since some players play the same games
    match_table.drop_duplicates(keep='first', inplace=True)
    # match_table.to_csv("./csv_files/saved_match_table.csv")
    return match_table


def save_chall_participant_tables(puuid_list):
    """
    Save tables for "amount" number of challenger players.
    :param amount: an integer representing the number of players that will be looped over.
    :return: participant_table dataframe
            The participant_table is a table of all the participants in each match in the match_table above.
            Each row in the participant table will contain info about the stats of a specific player in a specific
            match.
    """
    match_hists = []
    for puuid in puuid_list:
        match_hists.append(get_matches.get_match_history(puuid))
        print(type(match_hists[-1]))

    # flatten the 2D array
    match_hists = list(chain.from_iterable(match_hists))

    # initial pandas df
    participant_table = pd.DataFrame()

    # loop through match_ids and add all the participants from each match as a row in the participant table
    for match_id in match_hists:
        participant_table = pd.concat([participant_table, construct_tables.get_participant_table(match_id)])
        # participant_table.drop_duplicates(keep='first', inplace=True)
        if participant_table is None:
            return None

    return participant_table

def ingest_tables(amount=20):
    
    # get a list of summoner names that are in challenger
    print("Collecting Challenger Players...")
    try:
        sum_list = get_summoners.get_challenger_players()
    except:
        raise Exception('Failed to retrieve challenger players.')

    print("Challenger Players Collected!")

    print("Finding puuids...")
    try:
        puuid_list = []
        for summoner in sum_list[0:min(amount, len(sum_list))]:
            puuid_list.append(get_summoners.get_puuid(summoner))
    except:
        raise Exception('Failed to retrieve player puuids.')
    print("Puuids found!")

    print("Saving Match Tables...")
    match_table = save_chall_match_tables(puuid_list)
    print("Match Tables Complete!")

    print("Saving Participant Tables...")
    participant_table = save_chall_participant_tables(puuid_list)
    participant_table.drop_duplicates(subset=['summonerName', 'match_id'], keep='first', inplace=True)
    print("Participant Tables Complete!")


    return match_table, participant_table