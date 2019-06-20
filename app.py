import logging

from telegram.ext import Updater,  MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import random
from popug import images, config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
conf = config.load()


@run_async
def compliment(bot, update):
    logger.info('Got message: "' + update.message.text + '"')
    if update.message.text.lower().startswith("попуг скажи"):
        photo = images.stolen_letter(
            update.message.text.lower().replace("попуг скажи", ""))
        bot.sendPhoto(update.message.chat_id, photo=photo)
    elif update.message.text.lower().startswith("попуг покажи друга"):
        photo = images.random_friend()
        if photo == None:
            logger.warn("Something went wrong, check messages above")
        else:
            bot.sendPhoto(update.message.chat_id, photo=photo)
    # break


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(conf["token"], workers=32)

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
