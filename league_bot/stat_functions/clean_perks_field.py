

def separate_perk_fields(perks_field):
    print(perks_field.keys())
    perks = perks_field['styles']
    stat = perks_field['statPerks']
    print(perks)
    print(stat)
    return perks, stat

def clean_perks(perks_field):
    print(perks_field)
    perks_dict = {
        "major_rune_cat": None,
        "major_rune_specialty": None,
        "major_rune_1": None,
        "major_rune_2": None,
        "major_rune_3": None,

        "minor_rune_cat": None,
        "minor_rune_1": None,
        "minor_rune_2": None,

    }
    perks_dict['major_rune_cat'] = perks_field[0]['style']
    perks_dict['minor_rune_cat'] = perks_field[1]['style']
    
    major_rune_selections = perks_field[0]['selections']
    minor_rune_selections = perks_field[1]['selections']

    perks_dict['major_rune_specialty'] = major_rune_selections[0]['perk']
    perks_dict['major_rune_1'] = major_rune_selections[1]['perk']
    perks_dict['major_rune_2'] = major_rune_selections[2]['perk']
    perks_dict['major_rune_3'] = major_rune_selections[3]['perk']

    perks_dict['minor_rune_1'] = minor_rune_selections[0]['perk']
    perks_dict['minor_rune_2'] = minor_rune_selections[1]['perk']
    
    return perks_dict