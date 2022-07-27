from multiprocessing.dummy import Array
from numbers import Integral
from django.db import models
from django.forms import CharField, IntegerField, JSONField
from django.contrib.postgres.fields import ArrayField


class Match(models.Model):
    match = models.CharField(primary_key = True, max_length=30, default=0)
    duration = models.IntegerField(null=True)
    start_time = models.BigIntegerField(null=True)
    game_mode = models.CharField(null=True, max_length=30)
    patch = models.CharField(null=True, max_length=30)
    insertion_date = models.DateTimeField(null=True)


class Champion(models.Model):
    champ_name = models.CharField(primary_key=True, max_length=50, default="Default name")
    champ_play_count = models.IntegerField(null=True, default=-1)
    champ_winrate = models.FloatField(null=True, default=-1)


class Items(models.Model):
    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=50, default="default")
    gold = models.IntegerField(null=True)
    tags = ArrayField(models.CharField(max_length=30), size=10)
    builds_into = ArrayField(models.CharField(max_length=30), size=10)


class Champion_Items(models.Model):
    info_key = models.CharField(primary_key=True, max_length=50, default="default000")
    champ_name = models.ForeignKey(Champion, on_delete=models.CASCADE, default="Default name")
    item_id = models.IntegerField(null=True)
    play_count = models.IntegerField(null=True)
    

class Participant(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default=0)
    # NOTE Change this part_puuid to a Foriegn Key reference when player table is made.
    part_puuid = models.CharField(null=False, max_length=200)
    insertion_date = models.DateTimeField(null=True)

    # kda things
    assists = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    double_kills = models.IntegerField(null=True)
    killing_sprees = models.IntegerField(null=True)
    kills = models.IntegerField(null=True)
    penta_kills = models.IntegerField(null=True)
    quadra_kills = models.IntegerField(null=True)
    total_time_spent_dead = models.IntegerField(null=True)
    triple_kills = models.IntegerField(null=True)
    
    # runes and perks
    perks = models.JSONField(null=True)

    # account meta data
    summoner_level = models.IntegerField(null=True)
    summoner_name = models.CharField(null=True, max_length=50)
    profile_icon = models.IntegerField(null=True)


    # largest
    largest_crit_strike = models.IntegerField(null=True)
    largest_killing_spree = models.IntegerField(null=True)
    longest_time_spent_living = models.IntegerField(null=True)

    # position use the team_position field in the actual dataset
    position_played = models.CharField(null=True, max_length=30)


    # PVE things
    baron_kills = models.IntegerField(null=True)
    dragon_kills = models.IntegerField(null=True)
    neutral_mionions_killed = models.IntegerField(null=True)
    objectives_stolen = models.IntegerField(null=True)
    objectives_stolen_assists = models.IntegerField(null=True)
    total_minions_killed = models.IntegerField(null=True)

    # firsts
    first_blood_assist = models.BooleanField(default=False)
    first_blood_kill = models.BooleanField(default=False)
    first_tower_assist = models.BooleanField(default=False)
    first_tower_kill = models.BooleanField(default=False)

    bounty_level = models.IntegerField(null=True)

    # champion info and xp
    champ_xp = models.IntegerField(null=True)
    champ_level = models.IntegerField(null=True)
    champ_id = models.IntegerField(null=True)
    champ_name = models.CharField(null=True, max_length=30)
    champ_transform = models.IntegerField(null=True)

    # consumables and wards?
    consumables_purchased = models.IntegerField(null=True)
    detector_wards_placed = models.IntegerField(null=True)
    site_wards_bought = models.IntegerField(null=True)
    vision_score = models.IntegerField(null=True)
    vision_wards_bought = models.IntegerField(null=True)
    wards_killed = models.IntegerField(null=True)
    wards_placed = models.IntegerField(null=True)

    # spell casts
    spell_1_casts = models.IntegerField(null=True)
    spell_2_casts = models.IntegerField(null=True)
    spell_3_casts = models.IntegerField(null=True)
    spell_4_casts = models.IntegerField(null=True)
    summoner_1_casts = models.IntegerField(null=True)
    summoner_1_id = models.IntegerField(null=True)
    summoner_2_casts = models.IntegerField(null=True)
    summoner_2_id = models.IntegerField(null=True)

    # damage/healing/cc
    damage_to_buildings = models.IntegerField(null=True)
    damage_to_objectives = models.IntegerField(null=True)
    damage_to_turrets = models.IntegerField(null=True)
    damage_self_mitigated = models.IntegerField(null=True)
    magic_damage_dealt = models.IntegerField(null=True)
    magic_damage_dealt_to_champs = models.IntegerField(null=True)
    magic_damage_taken = models.IntegerField(null=True)
    phys_damage_dealt = models.IntegerField(null=True)
    phys_damage_dealt_to_champs = models.IntegerField(null=True)
    phys_damage_taken = models.IntegerField(null=True)

    total_time_cc_dealt = models.IntegerField(null=True)

    total_damage_dealt = models.IntegerField(null=True)
    total_damage_dealt_to_champs = models.IntegerField(null=True)
    total_damage_shielded_for_teammates = models.IntegerField(null=True)
    total_damage_taken = models.IntegerField(null=True)
    true_damage_dealt = models.IntegerField(null=True)
    true_damage_dealt_to_champs = models.IntegerField(null=True)
    true_damage_taken = models.IntegerField(null=True)
    total_heal = models.IntegerField(null=True)
    total_heal_for_teammates = models.IntegerField(null=True)
    

    # win/loss meta data
    win = models.BooleanField(null=False)
    ended_in_early_surrender = models.BooleanField(default=False)
    ended_in_surrender = models.BooleanField(default=False)

    # team meta data
    team_id = models.IntegerField(null=True)
    team_early_surrendered = models.BooleanField(default=False)

    # gold
    gold_earned = models.IntegerField(null=True)
    gold_spent = models.IntegerField(null=True)

    # inhibs and nexus
    inhibitor_kills = models.IntegerField(null=True)
    inhibitor_takedowns = models.IntegerField(null=True)
    inhibitors_lost = models.IntegerField(null=True)
    nexus_kills = models.IntegerField(null=True)
    nexus_lost = models.IntegerField(null=True)
    nexus_takedowns = models.IntegerField(null=True)

    # turrets
    turret_kills = models.IntegerField(null=True)
    turret_takedowns = models.IntegerField(null=True)
    turrets_lost = models.IntegerField(null=True)

    #items
    item0 = models.IntegerField(null=True)
    item1 = models.IntegerField(null=True)
    item2 = models.IntegerField(null=True)
    item3 = models.IntegerField(null=True)
    item4 = models.IntegerField(null=True)
    item5 = models.IntegerField(null=True)
    items_purchased = models.IntegerField(null=True)

    # item build
    @property
    def item_build(self):
        item_build  = {
            'item0': self.item0,
            'item1': self.item1,
            'item2': self.item2,
            'item3': self.item3,
            'item4': self.item4,
            'item5': self.item5,
        }
        return item_build








    
    






