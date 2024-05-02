from __future__ import annotations
import logging
from typing import Dict

from src.actions.callback.answer_callback import AnswerCallback
from src.repositories.api_repository import ApiRepository
from src.repositories.database_repository import DatabaseRepository
from src.repositories.repository import Repository
from src.facades.env import Env
from src.models.bot.bot import Bot
from src.mediators.query_mediators.audio_query_mediator import AudioQueryMediator
from src.mediators.query_mediators.video_query_mediator import VideoQueryMediator
from src.mediators.query_mediators.photo_query_mediator import PhotoQueryMediator
from src.mediators.query_mediators.text_query_mediator import TextQueryMediator
from src.actions.utility.user_data_updater import UserDataUpdater
from src.models.utility.state_data import StateData
from src.mediators.query_mediator import QueryMediator
from src.mediators.variable_mediator import VariableMediator
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
    app: Application

    def __init__(self, bot_id: int) -> None:
        self.bot_id = bot_id

    def register_variables(self) -> Bot_6:
        """Register variables"""
        self.variables = (
            VariableMediator().read_config().register_variables().get_variables()
        )
        return self

    def init_repository(self) -> Bot_6:
        """Create repository based on the environment"""
        if Env().repository == RepositoryTypes.DATABASE:
            ## database-repository
            self.repository = DatabaseRepository()
        else:
            ## api-repository
            self.repository = ApiRepository()
        return self

    def create_session_data(self) -> Bot_6:
        """Create new session and state_data"""
        username = "EMPTY"
        if self.update.effective_user and self.update.effective_user.username:
            username = self.update.effective_user.username
        session_id = self.repository.request_session(
            bot_id=self.bot.id, telegram_id=username
        )
        UserDataUpdater.update(
            self.context,
            StateData(
                bot_id=self.bot.id,
                started=True,
                session_id=session_id,
                bot_name=self.bot.name,
            ),
        )
        return self

    def create_bot_instance(self) -> Bot_6:
        self.bot = self.repository.get_me(self.bot_id)
        return self

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # starting a fresh user_data
        self.backup(update, context).create_session_data()
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

    def backup(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Bot_6:
        self.update = update
        self.context = context
        return self

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

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        print(f"error occured {str(context.error)}, go to start")
        if isinstance(update, Update):
            await AnswerCallback.with_update(self.update)
            await self.start(update, context)

    def build_application(self) -> Bot_6:
        """Create the application"""
        self.app = Application.builder().token(self.bot.token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CommandHandler("stop", self.stop))
        self.app.add_handler(CallbackQueryHandler(self.callback_query))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.text_query)
        )
        self.app.add_handler(MessageHandler(filters.PHOTO, self.photo_query))
        self.app.add_handler(
            MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, self.video_query)
        )
        self.app.add_handler(
            MessageHandler(filters.VOICE | filters.AUDIO, self.audio_query)
        )
        self.app.add_error_handler(self.error_handler)
        return self

    def run(self) -> None:
        """Run the bot."""
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main(bot_id: int):
    Bot_6(
        bot_id=bot_id
    ).register_variables().init_repository().create_bot_instance().build_application().run()
