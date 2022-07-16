import boto3
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_champion_stat_card(champ_row):
    champ_winrate = round(champ_row['champ_winrate'] * 100, 2)
    champ_play_count = champ_row['champ_play_count']

    s3_resource = boto3.resource('s3')

    stat_card = Image.open("league_bot/static_images/backdrop.jpeg")
    print(stat_card.size)
    draw = ImageDraw.Draw(stat_card)
    number_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Regular.ttf", 100)
    label_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Bold.otf", 25)
    # Draw winrate text and number
    draw.text((20, 20),f"{champ_winrate}%",(115,91, 48),font=number_font)
    draw.text((70, 120),f"WINRATE",(115,91, 48),font=label_font)

    # Draw in champ_playcount and text
    draw.text((20, 300),f"{champ_play_count}",(115,91, 48),font=number_font)
    draw.text((20, 400),f"MATCHES",(115,91, 48),font=label_font)
    
    if champ_row['champ_name'] != 'MonkeyKing':
        champ_name = champ_row['champ_name']
    else:
        champ_name = "Wukong"
    stat_card.save(f"league_bot/tmp_images/champ_stat_cards/{champ_name}.png", "PNG")

    return champ_name