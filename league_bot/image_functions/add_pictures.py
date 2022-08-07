from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont
import boto3
import os


def add_winrate_playcount(stat_card, champ_winrate, champ_play_count):
    """
    :param stat_card: The PIL object to be drawn onto
    :param champ_winrate: The winrate of the champion 
    :param champ_play_count: The number of games the champion has been recorded playing. 
    """
    draw = ImageDraw.Draw(stat_card)
    number_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Regular.ttf", 100)
    label_font = ImageFont.truetype("league_bot/fonts/Friz_Quadrata_Bold.otf", 25)
    # Draw winrate text and number
    draw.text((20, 20),f"{champ_winrate}%",(115,91, 48),font=number_font)
    draw.text((70, 120),f"WINRATE",(115,91, 48),font=label_font)

    # Draw in champ_playcount and text
    draw.text((20, 300),f"{champ_play_count}",(115,91, 48),font=number_font)
    draw.text((20, 400),f"MATCHES",(115,91, 48),font=label_font)
    return stat_card


def add_items(build_dict, stat_card):

    if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/item_pics"):
        try:
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "item_pics")
            os.mkdir(path)
        except FileExistsError:
            path = os.path.join(path, "item_pics")
            os.mkdir(path)

    s3_resource = boto3.resource('s3')
    print(build_dict['boots/item5']['item_id_id'])
    boots_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['boots/item5']['item_id_id']}/{build_dict['boots/item5']['item_id_id']}.png")
    boots_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['boots/item5']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['boots/item5']['item_id_id']}.png")
    starting_y = 200
    increment_y = 150

    x_pos, y_pos = (starting_y+(increment_y*1),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))

    mystic_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['mythic']['item_id_id']}/{build_dict['mythic']['item_id_id']}.png")
    mystic_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['mythic']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['mythic']['item_id_id']}.png")
    x_pos, y_pos = (starting_y+(increment_y*2),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))

    item1_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['item1']['item_id_id']}/{build_dict['item1']['item_id_id']}.png")
    item1_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['item1']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['item1']['item_id_id']}.png")
    x_pos, y_pos = (starting_y+(increment_y*3),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))

    item2_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['item2']['item_id_id']}/{build_dict['item2']['item_id_id']}.png")
    item2_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['item2']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['item2']['item_id_id']}.png")
    x_pos, y_pos = (starting_y+(increment_y*4),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))

    item3_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['item3']['item_id_id']}/{build_dict['item3']['item_id_id']}.png")
    item3_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['item3']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['item3']['item_id_id']}.png")
    x_pos, y_pos = (starting_y+(increment_y*5),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))

    item4_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"item_pics/{build_dict['item4']['item_id_id']}/{build_dict['item4']['item_id_id']}.png")
    item4_object.download_file(f"league_bot/tmp_images/item_pics/{build_dict['item4']['item_id_id']}.png")
    item = Image.open(f"league_bot/tmp_images/item_pics/{build_dict['item4']['item_id_id']}.png")
    x_pos, y_pos = (starting_y+(increment_y*6),550)
    width, height = item.size
    item = item.resize((round(width*1.5), round(height*1.5)))
    stat_card.paste(item, (x_pos, y_pos))


def add_runes(rune_dict, stat_card):

    if not os.path.isdir(f"/{os.getenv('ROOT_DIR')}/league_bot/tmp_images/rune_pics"):
        try:
            path = os.path.join(f"/{os.getenv('ROOT_DIR')}/league_bot", "tmp_images")
            os.mkdir(path)
            path = os.path.join(path, "rune_pics")
            os.mkdir(path)
        except FileExistsError:
            path = os.path.join(path, "rune_pics")
            os.mkdir(path)

    s3_resource = boto3.resource('s3')
    # add major specialty
    major_cat_id = rune_dict['perks']['major_rune_cat']
    major_cat_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{major_cat_id}/{major_cat_id}.png")
    major_cat_object.download_file(f"league_bot/tmp_images/rune_pics/{major_cat_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{major_cat_id}.png")
    x_pos, y_pos = (500,0)
    width, height = rune.size
    rune = rune.resize((round(width*2), round(height*2)))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))


    major_specialty_id = rune_dict['perks']['major_rune_specialty']
    major_specialty_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{major_specialty_id}/{major_specialty_id}.png")
    major_specialty_object.download_file(f"league_bot/tmp_images/rune_pics/{major_specialty_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{major_specialty_id}.png")
    x_pos, y_pos = (500,50)
    width, height = rune.size
    rune = rune.resize((round(width*0.5), round(height*0.5)))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))


    major_rune_id = rune_dict['perks']['major_rune_1']
    major_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{major_rune_id}/{major_rune_id}.png")
    major_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    x_pos, y_pos = (500,100)
    width, height = rune.size
    rune = rune.resize((64, 64))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))

    major_rune_id = rune_dict['perks']['major_rune_2']
    major_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{major_rune_id}/{major_rune_id}.png")
    major_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    x_pos, y_pos = (500,150)
    width, height = rune.size
    rune = rune.resize((64, 64))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))

    major_rune_id = rune_dict['perks']['major_rune_3']
    major_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{major_rune_id}/{major_rune_id}.png")
    major_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{major_rune_id}.png")
    x_pos, y_pos = (500,200)
    width, height = rune.size
    rune = rune.resize((64, 64))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))

    minor_cat_id = rune_dict['perks']['minor_rune_cat']
    minor_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{minor_cat_id}/{minor_cat_id}.png")
    minor_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{minor_cat_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{minor_cat_id}.png")
    x_pos, y_pos = (800,50)
    width, height = rune.size
    rune = rune.resize((round(width), round(height)))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))


    minor_rune_id = rune_dict['perks']['minor_rune_1']
    minor_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{minor_rune_id}/{minor_rune_id}.png")
    minor_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{minor_rune_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{minor_rune_id}.png")
    x_pos, y_pos = (800,100)
    width, height = rune.size
    rune = rune.resize((64, 64))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))

    minor_rune_id = rune_dict['perks']['minor_rune_2']
    minor_rune_object = s3_resource.Object(bucket_name="league-bot-image-bucket", key=f"rune_pics/{minor_rune_id}/{minor_rune_id}.png")
    minor_rune_object.download_file(f"league_bot/tmp_images/rune_pics/{minor_rune_id}.png")
    rune = Image.open(f"league_bot/tmp_images/rune_pics/{minor_rune_id}.png")
    x_pos, y_pos = (800,200)
    width, height = rune.size
    rune = rune.resize((64, 64))
    stat_card.paste(rune, (x_pos, y_pos), rune.convert('RGBA'))
    pass
