import pandas as pd


from .api_functions import get_summoners, get_matches

"""
A module which takes a summoner object as input and constructs all the tables corresponding to that summoner
and the their match history. The construction of these table is overseen by the get_all_tables function
which uses helper functions that do the actual construction of each respective table.
"""
class GetPuuidFailed(Exception):
    pass


def get_match_table(puuid):
    """
    Return a match_table for the entries in the players match history
    :param summoner_name: the name of a single summoner
    :return: pandas df representing the match table
    """

    if puuid is None:
        raise GetPuuidFailed

    match_hist_ids = get_matches.get_match_history(puuid=puuid, length=20)
    if match_hist_ids is None:
        return None

    match_table = calc_match_table(match_hist_ids)
    print(f"Completed Match Table for puuid: {puuid}")

    return match_table


def get_participant_table(match_id):
    """
    Return a participant table containing the stats for all the participants in a single
    match.
    :param match_id: the match id of the match that the participant table refers to.
    :return: pandas df representing the participant table
    """

    match_object = get_matches.get_match_details(match_id)
    if match_object is None:
        print("Match Object is None")
        return None

    participant_table = calc_participant_table(match_object)

    return participant_table


def calc_match_table(match_hist_ids):
    """
    Helper function.
    Does the heavy lifting to construct the match table.

    :param match_hist_ids: The list of match ids in the summoner's history. This is calculated
        from the main get_match_table function and then past in here.
    :return: A large pandas dataframe containing information about each match in a single row.
    """
    match_table = pd.DataFrame(columns=["duration", "start_time", "game_mode", "patch"])
    
    for match_id in match_hist_ids:
        match_object = get_matches.get_match_details(match_id=match_id)
        if match_object is None:
            continue
        row_values = {"match_id": match_object["metadata"]['matchId'],
                      "duration": match_object['info']['gameDuration'],
                      "start_time": match_object['info']['gameStartTimestamp'],
                      "game_mode": match_object['info']['gameMode'],
                      "patch": match_object['info']['gameVersion'][:4]}
        match_row = pd.Series(row_values, name=match_object['metadata']['matchId'])
        match_table = match_table.append(match_row)

    return match_table


def calc_participant_table(match_object):
    """
    Helper function.
    Does the heavy lifting to construct the participant table.

    :param match_object: A single json object representing the details of a given match.
    :return: A pandas dataframe where each row contains the stats of a single participant in the
    given match.
    """
    participant_table = pd.DataFrame(columns=list(match_object['info']['participants'][0].keys()))
    match_id = match_object['metadata']['matchId']

    for (part_puuid, part) in zip(match_object['metadata']['participants'], match_object['info']['participants']):
        row_values = part
        part_row = pd.Series(row_values, name=match_id)
        part_row['part_puuid'] = part_puuid
        part_row['match_id'] = match_id
        participant_table = participant_table.append(part_row)
        print()

    print("Construct Participant Table")
    if "challenges" in participant_table:
        return participant_table.drop(['challenges'], axis=1)
    else:
        print('NO CHALLENGES COLUMN, RETURNING NONE')
        return None


def calc_summoner_table(match_hist):
    summoner_table = pd.DataFrame(columns=[])
    return summoner_table


def calc_team_table(match_hist):
    team_table = pd.DataFrame(columns=[])
    return team_table
