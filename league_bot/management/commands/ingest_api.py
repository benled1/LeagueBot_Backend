import pandas as pd
import django_subcommands
from django.utils import timezone

from django.core.management.base import BaseCommand
from datetime import datetime
from league_bot.ingest_functions.save_tables import ingest_tables
from league_bot.models import Match, Participant
from django.db.utils import IntegrityError



def insert_match_table(match_table_row):
    try:
        print(f"Inserting Match model {match_table_row['match_id']}...")
        match_object_row = Match.objects.create(
            # this is the match_id but since its index it is unnamed
            match = match_table_row['match_id'],
            duration = match_table_row['duration'],
            start_time = match_table_row['start_time'],
            game_mode = match_table_row['game_mode'],
            patch = match_table_row['patch'],
            insertion_date = timezone.now()
        )
        return match_object_row
    except IntegrityError:
        return "Failed"
    
def insert_part_table(part_table_row):
    try:
        match_reference = Match.objects.get(match=part_table_row['match_id'])
    except:
        print(f"Failed to match the part_row to a match in the match table: {part_table_row['match_id']}")
        return "Failed"

    try:
        print(f"Inserting Participant model {part_table_row['summonerName']}")
        part_object_row = Participant.objects.create(

            insertion_date = timezone.now(),
            match = match_reference,
            part_puuid = part_table_row['part_puuid'],
            win = part_table_row['win'],
            assists = part_table_row['assists'],
            deaths = part_table_row['deaths'],
            double_kills = part_table_row['doubleKills'],
            killing_sprees = part_table_row['killingSprees'],
            kills = part_table_row['kills'],
            penta_kills = part_table_row['pentaKills'],
            quadra_kills = part_table_row['quadraKills'],
            total_time_spent_dead = part_table_row['totalTimeSpentDead'],
            triple_kills = part_table_row['tripleKills'],
            perks = part_table_row['perks'],
            summoner_level = part_table_row['summonerLevel'],
            summoner_name = part_table_row['summonerName'],
            profile_icon = part_table_row['profileIcon'],
            largest_crit_strike = part_table_row['largestCriticalStrike'],
            largest_killing_spree = part_table_row['largestKillingSpree'],
            longest_time_spent_living = part_table_row['longestTimeSpentLiving'],
            position_played = part_table_row['teamPosition'],
            baron_kills = part_table_row['baronKills'],
            dragon_kills = part_table_row['dragonKills'],
            neutral_mionions_killed = part_table_row['neutralMinionsKilled'],
            objectives_stolen = part_table_row['objectivesStolen'],
            objectives_stolen_assists = part_table_row['objectivesStolenAssists'],
            total_minions_killed = part_table_row['totalMinionsKilled'],
            first_blood_assist = part_table_row['firstBloodAssist'],
            first_blood_kill = part_table_row['firstBloodKill'],
            first_tower_assist = part_table_row['firstTowerAssist'],
            first_tower_kill = part_table_row['firstTowerKill'],
            bounty_level = part_table_row['bountyLevel'],
            champ_xp = part_table_row['champExperience'],
            champ_level = part_table_row['champLevel'],
            champ_id = part_table_row['championId'],
            champ_name = part_table_row['championName'],
            champ_transform = part_table_row['championTransform'],
            consumables_purchased = part_table_row['consumablesPurchased'],
            detector_wards_placed = part_table_row['detectorWardsPlaced'],
            site_wards_bought = part_table_row['sightWardsBoughtInGame'],
            vision_score = part_table_row['visionScore'],
            vision_wards_bought = part_table_row['visionWardsBoughtInGame'],
            wards_killed = part_table_row['wardsKilled'],
            wards_placed = part_table_row['wardsPlaced'],
            spell_1_casts = part_table_row['spell1Casts'],
            spell_2_casts = part_table_row['spell2Casts'],
            spell_3_casts = part_table_row['spell3Casts'],
            spell_4_casts = part_table_row['spell4Casts'],
            summoner_1_casts = part_table_row['summoner1Casts'],
            summoner_1_id = part_table_row['summoner1Id'],
            summoner_2_casts = part_table_row['summoner2Casts'],
            summoner_2_id = part_table_row['summoner2Id'],
            damage_to_buildings = part_table_row['damageDealtToBuildings'],
            damage_to_objectives = part_table_row['damageDealtToObjectives'],
            damage_to_turrets = part_table_row['damageDealtToTurrets'],
            damage_self_mitigated = part_table_row['damageSelfMitigated'],
            magic_damage_dealt = part_table_row['magicDamageDealt'],
            magic_damage_dealt_to_champs = part_table_row['magicDamageDealtToChampions'],
            magic_damage_taken = part_table_row['magicDamageTaken'],
            phys_damage_dealt = part_table_row['physicalDamageDealt'],
            phys_damage_dealt_to_champs = part_table_row['physicalDamageDealtToChampions'],
            phys_damage_taken = part_table_row['physicalDamageTaken'],
            total_time_cc_dealt = part_table_row['totalTimeCCDealt'],
            total_damage_dealt = part_table_row['totalDamageDealt'],
            total_damage_dealt_to_champs = part_table_row['totalDamageDealtToChampions'],
            total_damage_shielded_for_teammates = part_table_row['totalDamageShieldedOnTeammates'],
            total_damage_taken = part_table_row['totalDamageTaken'],
            true_damage_dealt = part_table_row['trueDamageDealt'],
            true_damage_dealt_to_champs = part_table_row['trueDamageDealtToChampions'],
            true_damage_taken = part_table_row['trueDamageTaken'],
            total_heal = part_table_row['totalHeal'],
            total_heal_for_teammates = part_table_row['totalHealsOnTeammates'],
            ended_in_early_surrender = part_table_row['gameEndedInEarlySurrender'],
            ended_in_surrender = part_table_row['gameEndedInSurrender'],
            team_id = part_table_row['teamId'],
            team_early_surrendered = part_table_row['teamEarlySurrendered'],
            gold_earned = part_table_row['goldEarned'],
            gold_spent = part_table_row['goldSpent'],
            inhibitor_kills = part_table_row['inhibitorKills'],
            inhibitor_takedowns = part_table_row['inhibitorTakedowns'],
            inhibitors_lost = part_table_row['inhibitorsLost'],
            nexus_kills = part_table_row['nexusKills'],
            nexus_lost = part_table_row['nexusLost'],
            nexus_takedowns = part_table_row['nexusTakedowns'],
            turret_kills = part_table_row['turretKills'],
            turret_takedowns = part_table_row['turretTakedowns'],
            turrets_lost = part_table_row['turretsLost'],
            item0 = part_table_row['item0'],
            item1 = part_table_row['item1'],
            item2 = part_table_row['item2'],
            item3 = part_table_row['item3'],
            item4 = part_table_row['item4'],
            item5 = part_table_row['item5'],
            items_purchased = part_table_row['itemsPurchased']

        )
        return part_object_row
    except IntegrityError:
        pass


class Challengers(BaseCommand):
    """
    Create entries for a number of challenger players taken from the challenger api call.
    This creates entries in the match table, participants table and summoners table.
    """
    help = "ingest the info on challenger players and their games"
    def handle(self, *args, **kwargs):

        match_table, part_table = ingest_tables(amount=10)

        match_dict = match_table.to_dict('records')
        for row in match_dict:
            insert_match_table(row)

        part_dict = part_table.to_dict('records')
        for row in part_dict:
            insert_part_table(row)


class Command(django_subcommands.SubCommands):
    subcommands = {"challengers": Challengers}

