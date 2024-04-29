from __future__ import annotations
import logging
from typing import Dict
from src.repositories.api_repository import ApiRepository
from src.repositories.database_repository import DatabaseRepository
from src.repositories.repository import Repository
from src.facades.env import Env
from src.models.bot.bot import Bot
from src.models.bot.bot_cfg import BotCfg
from src.mediators.query_mediators.audio_query_mediator import AudioQueryMediator
from src.mediators.query_mediators.video_query_mediator import VideoQueryMediator
from src.mediators.query_mediators.photo_query_mediator import PhotoQueryMediator
from src.mediators.query_mediators.text_query_mediator import TextQueryMediator
from src.actions.user_data_updater import UserDataUpdater
from src.models.utility.state_data import StateData
from src.mediators.query_mediator import QueryMediator
from src.mediators.variable_mediator import VariableMediator
from src.helpers.config.bot_config import BotConfig
from src.types.variable import Variable
from src.types.repository_types import RepositoryTypes
from telegram import Update
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
    # env: BotEnvData
    variables: Dict[str, Variable]
    bot: Bot
    repository: Repository

    def read_environments(self) -> Bot_6:
        # self.env = BotEnvData(**BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_6:
        self.cfg = BotCfg(**BotConfig(__file__).read("cfg"))
        self.variables = (
            VariableMediator().read_config().register_variables().get_variables()
        )
        return self

    def init_repository(self) -> Bot_6:
        if Env().repository == RepositoryTypes.DATABASE:
            ## database-repository
            self.repository = DatabaseRepository()
        else:
            ## api-repository
            self.repository = ApiRepository()
        return self

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # starting a fresh user_data
        self.backup(update, context)
        UserDataUpdater.update(context, StateData(bot_id=self.bot.id))
        await self.procedure(
            QueryMediator.from_command(update, context, self.repository)
        )

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.backup(update, context)
        await self.procedure(
            QueryMediator.from_callback(update, context, self.repository)
        )

    async def procedure(self, query_mediator: QueryMediator):
        query_mediator.detect_page()
        query_mediator.validate_data()
        query_mediator.map_data()
        query_mediator.store_data()
        query_mediator.create_content(self.variables)
        query_mediator.create_keyboard(self.variables)
        await query_mediator.answer()
        query_mediator.update_user_data(self.context)

    def backup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context

    async def text_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.backup(update, context)
        mediator = TextQueryMediator.build(update, context, self.repository)
        mediator.initialize_chain(self.variables)
        await self.procedure(mediator)

    async def photo_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.backup(update, context)
        mediator = await PhotoQueryMediator.build(update, context, self.repository)
        mediator.initialize_chain(self.variables)
        await self.procedure(mediator)

    async def video_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.backup(update, context)
        mediator = await VideoQueryMediator.build(update, context, self.repository)
        mediator.initialize_chain(self.variables)
        await self.procedure(mediator)

    async def audio_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.backup(update, context)
        mediator = await AudioQueryMediator.build(update, context, self.repository)
        mediator.initialize_chain(self.variables)
        await self.procedure(mediator)

    def run(self) -> None:
        """Run the bot."""
        # Create the Application and pass it your bot's token.
        self.bot = self.repository.get_me(self.cfg.id)
        application = Application.builder().token(self.bot.token).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(CommandHandler("stop", self.stop))
        application.add_handler(CallbackQueryHandler(self.callback_query))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_query)
        )
        application.add_handler(MessageHandler(filters.PHOTO, self.photo_query))
        application.add_handler(
            MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, self.video_query)
        )
        application.add_handler(
            MessageHandler(filters.VOICE | filters.AUDIO, self.audio_query)
        )

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    Bot_6().read_configs().init_repository().run()
