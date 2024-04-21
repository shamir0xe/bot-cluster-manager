from __future__ import annotations
import logging
from src.mediators.query_mediator import QueryMediator
from src.mediators.variable_mediator import VariableMediator
from src.helpers.config.bot_config import BotConfig
from src.types.bot_env_data import BotEnvData
from typing import Any, Dict, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class Bot_6:
    env: BotEnvData

    def read_environments(self) -> Bot_6:
        self.env = BotEnvData.from_dict(BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_6:
        self.variables = (
            VariableMediator().read_config().register_variables().get_variables()
        )
        return self

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        mediator = QueryMediator.from_callback(update, context)
        mediator = mediator.validate_data()
        mediator = mediator.map_data()
        mediator = mediator.store_data()
        mediator = mediator.create_content(self.variables)
        mediator = mediator.create_keyboard()
        mediator = await mediator.answer()

    async def message_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    def run(self) -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.

        application = Application.builder().token(self.env.token).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(CommandHandler("stop", self.stop))
        application.add_handler(CallbackQueryHandler(self.callback_query))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_query)
        )

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    Bot_6().read_configs().read_environments().run()
