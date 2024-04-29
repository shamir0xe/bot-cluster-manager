from typing import Optional
from telegram import InlineKeyboardMarkup, Update


class MessageEdit:
    @staticmethod
    async def with_update(
        update: Update, text: str = "", keyboard: Optional[InlineKeyboardMarkup] = None
    ):
        if update.callback_query:
            if keyboard:
                await update.callback_query.edit_message_text(
                    text=text, reply_markup=keyboard
                )
            else:
                await update.callback_query.edit_message_text(text=text)
