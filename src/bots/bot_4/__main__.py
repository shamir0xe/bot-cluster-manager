from __future__ import annotations
from pydantic import BaseModel
from pylib_0xe.data.data_transfer_object import DataTransferObject
from pylib_0xe.path.path_helper import PathHelper
from src.helpers.config.bot_config import BotConfig
from src.types.bot_env_data import BotEnvData
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    logger.info("here we call message handler again, %s", "photo")
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    print(photo_file)
    print(photo_file.file_id)
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    logger.info("here we call message handler again, %s", "location")
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def get_photo(bot: Bot):
    logger.info("asdfasdfa")
    print("sadfasdf")
    file = await bot.get_file(
        "AgACAgQAAxkBAAMhZiJ5SwABBXz3LsV-wqsNY9IkLaQDAALKwTEb8SMYUX7VDlD2jMY2AQADAgADeAADNAQ"
    )
    print(file)
    print(file.file_id)


class Bot_4:
    env: BotEnvData

    def read_environments(self) -> Bot_4:
        self.env = BotEnvData.from_dict(BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_4:
        return self

    def run(self) -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(self.env.token).build()

        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
                PHOTO: [
                    MessageHandler(filters.PHOTO, photo),
                    CommandHandler("skip", skip_photo),
                ],
                LOCATION: [
                    MessageHandler(filters.LOCATION, location),
                    CommandHandler("skip", skip_location),
                ],
                BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        application.add_handler(conv_handler)
        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)

        # import asyncio
        # bot = Bot(self.env.token)
        # asyncio.run(get_photo(bot))
        #
        # while (True):
        #     import time
        #     time.sleep(1.)
        #     print('.')


def main():
    Bot_4().read_configs().read_environments().run()
