from __future__ import annotations
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)
from src.helpers.config.bot_config import BotConfig
from src.types.bot_env_data import BotEnvData
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Bot_1:
    env: BotEnvData
    bot: telegram.Bot

    def read_environments(self) -> Bot_1:
        self.env = BotEnvData.from_dict(BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_1:
        return self

    def run(self) -> None:
        # asyncio.run(self.main_procedure())
        self.main_procedure()

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(update.effective_chat, telegram.Chat):
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="hello there!"
            )

    async def caps_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(update.effective_chat, telegram.Chat):
            if context.args:
                text_caps = " ".join(context.args).upper()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=text_caps
                )

    async def echo_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(update.effective_chat, telegram.Chat):
            if update.message and update.message.text:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=update.message.text
                )

    async def unknown_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if isinstance(update.effective_chat, telegram.Chat):
            if update.message and update.message.text:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text="unknown command!"
                )

    async def inline_query_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if not update.inline_query or not update.inline_query.query:
            return
        query = update.inline_query.query
        results = []
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title="Caps",
                input_message_content=InputTextMessageContent(query.upper()),
            )
        )
        await context.bot.answer_inline_query(update.inline_query.id, results)

    def main_procedure(self):
        app = ApplicationBuilder().token(self.env.token).build()
        app.add_handler(CommandHandler("start", self.start_handler))
        app.add_handler(CommandHandler("caps", self.caps_handler))
        app.add_handler(InlineQueryHandler(self.inline_query_handler))
        app.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo_handler)
        )
        app.add_handler(MessageHandler(filters.COMMAND, self.unknown_handler))
        app.run_polling()

        # self.bot = telegram.Bot(self.env.token)
        # async with self.bot:
        #     print(await self.bot.get_me())
        #     updates = await self.bot.get_updates()
        #     for update_instance in updates:
        #         print(update_instance)
        #         if (
        #             update_instance.message is not None
        #             and update_instance.message.from_user is not None
        #         ):
        #             await self.bot.send_message(
        #                 text=f"Hi {update_instance.message.from_user.full_name}",
        #                 chat_id=update_instance.message.chat.id,
        #             )
        #


def main():
    Bot_1().read_configs().read_environments().run()
