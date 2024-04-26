from typing import Optional
from telegram import InlineKeyboardMarkup, Update


class MessageReply:
    @staticmethod
    async def with_update(
        update: Update, text: str = "", keyboard: Optional[InlineKeyboardMarkup] = None
    ):
        if update.message:
            if keyboard:
                await update.message.reply_text(text=text, reply_markup=keyboard)
            else:
                await update.message.reply_text(text=text)
