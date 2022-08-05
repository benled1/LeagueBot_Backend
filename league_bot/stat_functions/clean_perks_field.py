

def separate_perk_fields(perks_field):
    print(perks_field.keys())
    perks = perks_field['styles']
    stat = perks_field['statPerks']
    print(perks)
    print(stat)
    return perks, stat