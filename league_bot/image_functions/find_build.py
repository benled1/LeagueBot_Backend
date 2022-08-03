from league_bot.models import Champion_Items, Items
from django.db.models import Q



def find_best_boots(champ_name):
    all_boots = list(Items.objects.filter(tags__contains=["Boots"]).values())
    all_boot_ids = [item_dict['item_id'] for item_dict in all_boots]

    champion_boots = list(Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_boot_ids).order_by("-play_count").values())
    if champion_boots != []:
        best_boots = champion_boots[0]
        return best_boots
    
    return "no_boots"

def find_best_mythic(champ_name):
    all_mythics = list(Items.objects.filter(description__contains="rarityMythic").values())
    all_mythic_ids = [item_dict['item_id'] for item_dict in all_mythics]


    champion_mythic = Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_mythic_ids).order_by("-play_count").values()
    best_mythic = champion_mythic[0]
    return best_mythic

def find_best_full_items(champ_name, count=4):
    all_full_items = list(Items.objects.filter(builds_into=[]).filter(gold__gt=500).values()
                                        .filter(~Q(tags__contains=["Boots"]))
                                        .filter(~Q(description__contains="rarityMythic")))
    all_full_item_ids = [item_dict['item_id'] for item_dict in all_full_items]

    champion_full_items = list(Champion_Items.objects.filter(champ_name=champ_name).filter(item_id__in=all_full_item_ids).order_by("-play_count").values())
    best_full_items = champion_full_items[:count]
    return best_full_items
    

def get_item_build(champ_name):
    """
    TODO:
    - Finish the find best boots function
    - Finish the find mythic function (take into consideration that Ornn items have different item ids as
        the regular mythic even though same item.)
    - Finish finding remaining full items function
    - NOTE: Mythic items say mythic in the plaintext field, try adding that to model,
    - NOTE: Ornn upgrades have reuired_Ally: Ornn in dict, add that to model too
    - NOTE: do some check to see if Ornn item and then match it to the actual item.
    - NOTE: If all else fails, just hardcode a dict or smth >:)
    """
    best_boots = find_best_boots(champ_name=champ_name)
    best_mythic = find_best_mythic(champ_name=champ_name)
    if best_boots == "no_boots":
        best_full_items = find_best_full_items(champ_name=champ_name, count=5)
        best_build_dict = {
        "boots/item5": best_full_items[4],
        "mythic": best_mythic,
        "item1": best_full_items[0],
        "item2": best_full_items[1],
        "item3": best_full_items[2],
        "item4": best_full_items[3],
    }
    else:
        best_full_items = find_best_full_items(champ_name=champ_name)
        best_build_dict = {
        "boots/item5": best_boots,
        "mythic": best_mythic,
        "item1": best_full_items[0],
        "item2": best_full_items[1],
        "item3": best_full_items[2],
        "item4": best_full_items[3],
    }

    
    return best_build_dict