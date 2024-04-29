from telegram import Update


class AnswerCallback:
    @staticmethod
    async def with_update(update: Update):
        if update.callback_query:
            await update.callback_query.answer()
