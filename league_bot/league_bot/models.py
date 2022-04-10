from numbers import Integral
from tkinter.tix import INTEGER
from django.db import models
from django.forms import CharField, IntegerField, JSONField

class Test(models.Model):
    first_attr = models.CharField(max_length=30)


class Match(models.Model):
    match_id = models.CharField(primary_key = True, max_length=30),
    duration = models.IntegerField(null=True),
    start_time = models.IntegerField(null=True),
    game_mode = models.CharField(null=True, max_length=30),
    patch = models.CharField(null=True, max_length=30),

# class Participant(models.Model):
#     match_id = models.ForeignKey(Match, on_delete=models.CASCADE),

#     # kda things
#     assists = models.IntegerField(null=True),
#     deaths = models.IntegerField(null=True),
#     double_kills = models.IntegerField(null=True),
#     killing_sprees = models.IntegerField(null=True),
#     kills = models.IntegerField(null=True),
#     penta_kills = models.IntegerField(null=True),
#     quadra_kills = models.IntegerField(null=True),
#     total_time_spent_dead = models.IntegerField(null=True),
#     triple_kills = models.IntegerField(null=True),
    

#     # runes and perks
#     perks = JSONField(),

#     # account meta data
#     puuid = models.CharField(null=True, max_length=50),
#     summoner_id = models.CharField(null=True, max_length=50),
#     summoner_level = models.IntegerField(null=True),
#     summoner_name = models.CharField(null=True, max_length=50),
#     profile_icon = models.IntegerField(null=True),


#     # largest
#     largest_crit_strike = models.IntegerField(null=True),
#     largest_killing_spree = models.IntegerField(null=True),
#     longest_time_spent_living = models.IntegerField(null=True),

#     # position use the team_position field in the actual dataset
#     position_played = models.CharField(null=True, max_length=30),


#     # PVE things
#     baron_kills = models.IntegerField(null=True),
#     dragon_kills = models.IntegerField(null=True),
#     neutral_mionions_killed = models.IntegerField(null=True),
#     objectives_stolen = models.IntegerField(null=True),
#     objectives_stolen_assists = models.IntegerField(null=True),
#     total_minions_killed = models.IntegerField(null=True),

#     # firsts
#     first_blood_assist = models.BooleanField(default=False),
#     first_blood_kill = models.BooleanField(default=False),
#     first_tower_assist = models.BooleanField(default=False),
#     first_tower_kill = models.BooleanField(default=False),

#     bounty_level = models.IntegerField(null=True),

#     # champion info and xp
#     champ_xp = models.IntegerField(null=True),
#     champ_level = models.IntegerField(null=True),
#     champ_id = models.IntegerField(null=True),
#     champ_name = models.CharField(null=True, max_length=30),
#     champ_transform = models.IntegerField(null=True),

#     # consumables and wards?
#     consumables_purchased = models.IntegerField(null=True),
#     detector_wards_placed = models.IntegerField(null=True),
#     site_wards_bought = models.IntegerField(null=True),
#     vision_score = models.IntegerField(null=True),
#     vision_wards_bought = models.IntegerField(null=True),
#     wards_killed = models.IntegerField(null=True),
#     wards_placed = models.IntegerField(null=True),

#     # spell casts
#     spell_1_casts = models.IntegerField(null=True),
#     spell_2_casts = models.IntegerField(null=True),
#     spell_3_casts = models.IntegerField(null=True),
#     spell_4_casts = models.IntegerField(null=True),
#     summoner_1_casts = models.IntegerField(null=True),
#     summoner_1_id = models.IntegerField(null=True),
#     summoner_2_casts = models.IntegerField(null=True),
#     summoner_2_id = models.IntegerField(null=True),

#     # damage/healing/cc
#     damage_to_buildings = models.IntegerField(null=True),
#     damage_to_objectives = models.IntegerField(null=True),
#     damage_to_turrets = models.IntegerField(null=True),
#     damage_self_mitigated = models.IntegerField(null=True),
#     magic_damage_dealt = models.IntegerField(null=True),
#     magic_damage_dealt_to_champs = models.IntegerField(null=True),
#     magic_damage_taken = models.IntegerField(null=True),
#     phys_damage_dealt = models.IntegerField(null=True),
#     phys_damage_dealt_to_champs = models.IntegerField(null=True),
#     phys_damage_taken = models.IntegerField(null=True),

#     total_time_cc_dealt = models.IntegerField(null=True),

#     total_damage_dealt = models.IntegerField(null=True),
#     total_damage_dealt_to_champs = models.IntegerField(null=True),
#     total_damage_shielded_for_teammates = models.IntegerField(null=True),
#     total_damage_taken = models.IntegerField(null=True),
#     true_damage_dealt = models.IntegerField(null=True),
#     true_damage_dealt_to_champs = models.IntegerField(null=True),
#     true_damage_taken = models.IntegerField(null=True),
#     total_heal = models.IntegerField(null=True),
#     total_heal_for_teammates = models.IntegerField(null=True),
    

#     # win/loss meta data
#     win = models.BooleanField(null=False)
#     ended_in_early_surrender = models.BooleanField(default=False),
#     ended_in_surrender = models.BooleanField(default=False),

#     # team meta data
#     team_id = models.IntegerField(null=True),
#     team_early_surrendered = models.BooleanField(default=False),

#     # gold
#     gold_earned = models.IntegerField(null=True),
#     gold_spent = models.IntegerField(null=True),

#     # inhibs and nexus
#     inhibitor_kills = models.IntegerField(null=True),
#     inhibitor_takedowns = models.IntegerField(null=True),
#     inhibitors_lost = models.IntegerField(null=True),
#     nexus_kills = models.IntegerField(null=True),
#     nexus_lost = models.IntegerField(null=True),
#     nexus_takedowns = models.IntegerField(null=True),

#     # turrets
#     turret_kills = models.IntegerField(null=True),
#     turret_takedowns = models.IntegerField(null=True),
#     turrets_lost = models.IntegerField(null=True),

#     #items
#     item0 = models.IntegerField(null=True),
#     item1 = models.IntegerField(null=True),
#     item2 = models.IntegerField(null=True),
#     item3 = models.IntegerField(null=True),
#     item4 = models.IntegerField(null=True),
#     item5 = models.IntegerField(null=True),
#     items_purchased = models.IntegerField(null=True),







    
    






