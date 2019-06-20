#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from textwrap import wrap
from io import BytesIO, BufferedReader, open
from PIL import Image, ImageFont, ImageDraw
from telegram.ext import Updater,  MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import random
import glob

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

font = ImageFont.truetype('./OpenSans-Bold.ttf', 82, encoding="utf-8")

def generate(message):
    message = message.lower().replace(u'e', '  ').replace(u'е', '  ')

    image = Image.open('./popug.png').convert('RGBA')

    draw = ImageDraw.Draw(image)

    comp = message.upper()
    lines = wrap(comp, 10)

    #draw.text((10, 10), str('\n'.join(lines)), font=font)

    for n, line in enumerate(lines):
        draw.text((550 - font.getsize(line)[0] / 2, 150 - (50 * len(lines))/2 + 100 * n), line, font=font, fill=(255,255,255))


   # image.save('test.png', 'PNG')

    bio = BytesIO()
    bio.name = 'compliment.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    return BufferedReader(bio)


@run_async
def compliment(bot, update):
    logger.info('Got message: "' + update.message.text + '"')
    if update.message.text.lower().startswith(u"попуг скажи"):
        photo = generate(update.message.text.lower().replace(u"попуг скажи", u""))
        bot.sendPhoto(update.message.chat_id, photo=photo)
    elif update.message.text.lower().startswith(u"попуг покажи друга"):
        photo = image()
        bot.sendPhoto(update.message.chat_id, photo=photo)
    #break


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def image():
    folder = './popug-images/*'
    a=random.choice(glob.glob(folder))

    return BufferedReader(open(a, 'rb'))

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('540376351:AAGcP9MkeZUuMHTo9kF8rwQqrTPwdmYIa0U', workers=32)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(MessageHandler((Filters.text), compliment))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(timeout=30)

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
