from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

class XPCard():
    def __init__(self):
        pass

    def BuildCard(user:str,rank:int,xp:int,next_level_xp:int,profile_bytes:BytesIO):
        font=ImageFont.load_default()
        
        profile_bytes = Image.open(profile_bytes)
        im = Image.new('RGBA', (400, 148), (44, 44, 44, 255))

        im_draw = ImageDraw.Draw(im)
        im_draw.text((154, 5), user, font=font, fill=(255, 255, 255, 255))

        rank_text = f'RANK {rank}'
        im_draw.text((154, 37), rank_text, font=font, fill=(255, 255, 255, 255))

        needed_xp = next_level_xp
        xp_text = f'{xp}/{needed_xp}'
        im_draw.text((154, 62), xp_text, font=font, fill=(255, 255, 255, 255))

        im_draw.rectangle((174, 95, 374, 125), fill=(64, 64, 64, 255))
        im_draw.rectangle((174, 95, 174+(int(xp/needed_xp*100))*2, 125), fill=(221, 221, 221, 255))

        im_draw.rectangle((0, 0, 148, 148), fill=(255, 255, 255, 255))
        im.paste(profile_bytes, (10, 10))

        buffer = BytesIO()
        im.save(buffer, 'png')
        buffer.seek(0)

        return buffer
