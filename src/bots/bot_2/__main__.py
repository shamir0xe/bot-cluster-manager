#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""This example showcases how PTBs "arbitrary callback data" feature can be used.

For detailed info on arbitrary callback data, see the wiki page at
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Arbitrary-callback_data

Note:
To use arbitrary callback data, you must install PTB via
`pip install "python-telegram-bot[callback-data]"`
"""
from __future__ import annotations
import logging
import os
from typing import List, Tuple, cast

from pydantic import BaseModel
from pylib_0xe.path.path_helper import PathHelper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
    PicklePersistence,
)

from src.helpers.config.bot_config import BotConfig
from src.types.bot_env_data import BotEnvData

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with 5 inline buttons attached."""
    number_list: List[int] = []
    await update.message.reply_text("Please choose:", reply_markup=build_keyboard(number_list))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the callback data cache"""
    context.bot.callback_data_cache.clear_callback_data()
    context.bot.callback_data_cache.clear_callback_queries()
    await update.effective_message.reply_text("All clear!")


def build_keyboard(current_list: List[int]) -> InlineKeyboardMarkup:
    """Helper function to build the next inline keyboard."""
    return InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(str(i), callback_data=(i, current_list)) for i in range(1, 6)]
    )


async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # Get the data from the callback_data.
    # If you're using a type checker like MyPy, you'll have to use typing.cast
    # to make the checker get the expected type of the callback_data
    number, number_list = cast(Tuple[int, List[int]], query.data)
    # append the number to the list
    number_list.append(number)

    await query.edit_message_text(
        text=f"So far you've selected {number_list}. Choose the next item:",
        reply_markup=build_keyboard(number_list),
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )

class Bot_2:
    env: BotEnvData

    def read_environments(self) -> Bot_2:
        self.env = BotEnvData.from_dict(BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_2:
        self.cfg = ConfigData(**BotConfig(__file__).read("config"))
        return self

    def run(self) -> None:
        """Run the bot."""
        # We use persistence to demonstrate how buttons can
        # still work after the bot was restarted
        print(self.cfg.model_dump())
        print(self.cfg.pickle.path)
        path = os.path.join(
            PathHelper(__file__, ["bot_2"]).root_path(), "bot_2", *self.cfg.pickle.path
        )
        print(path)
        persistence = PicklePersistence(filepath=path)
        # Create the Application and pass it your bot's token.
        application = (
            Application.builder()
            .token(self.env.token)
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("clear", clear))
        application.add_handler(
            CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
        )
        application.add_handler(CallbackQueryHandler(list_button))

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES) 

def main():
    Bot_2().read_configs().read_environments().run()


class ConfigData(BaseModel):
    class PickleData(BaseModel):
        path: List[str]

    pickle: PickleData
