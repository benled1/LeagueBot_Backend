class BadResponseGetChallengers(Exception):

    def __init__(self, code):
        self.status_code = code
    

class BadResponseGetPuuid(Exception):

    def __init__(self, code, player_name):
        self.status_code = code
        self.player_name = player_name

class BadResponseGetMatchHistory(Exception):

    def __init__(self, code, puuid):
        self.status_code = code
        self.puuid = puuid

class BadResponseGetMatchDetails(Exception):

    def __init__(self, code, match_id):
        self.status_code = code
        self.match_id = match_id

class PlayerQuoteFailed(Exception):
    
    def __init__(self, name, ):
        self.summoner_name = name

class PuuidQuoteFailed(Exception):

    def __init__(self, puuid):
        self.puuid = puuid

class MatchQuoteFailed(Exception):

    def __init__(self, match_id):
        self.match_id = match_id

class InvalidMatchType(Exception):

    def __init__(self, match_id, match_type):
        self.match_id = match_id
        self.match_type = match_type


