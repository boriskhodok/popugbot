import popug
from io import BytesIO, BufferedReader, open
from PIL import Image, ImageFont, ImageDraw
from textwrap import wrap
import random
from popug import config
import glob
import json
import os
import logging

conf = config.load()
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


font = ImageFont.truetype(conf["font"]["file"],
                          conf["font"]["size"], encoding="utf-8")


def stolen_letter(message):
    message = message.lower().replace(u'e', '  ').replace(u'е', '  ')

    image = Image.open(os.getcwd() + '/res/popug.png').convert('RGBA')

    draw = ImageDraw.Draw(image)

    comp = message.upper()
    lines = wrap(comp, 10)

    for n, line in enumerate(lines):
        draw.text((550 - font.getsize(line)[0] / 2, 150 - (
            50 * len(lines))/2 + 100 * n), line, font=font, fill=(255, 255, 255))

    bio = BytesIO()
    bio.name = 'compliment.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    return BufferedReader(bio)


def random_friend():
    try:
        friends_dir_name = conf["friendsDir"]
        if not os.path.exists(friends_dir_name):
            raise IOError("Directory with popug friends images doesn't exist")

        friends_dir = '%s/*' % friends_dir_name
        all_friends_files = glob.glob(friends_dir)

        if len(all_friends_files) == 0:
            raise FileNotFoundError("Directory %s is empty" % friends_dir)

        a = random.choice(glob.glob(friends_dir))

        return BufferedReader(open(a, 'rb'))
    except Exception as error:
        logger.warn(error)
