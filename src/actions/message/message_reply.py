from typing import Optional
from telegram import InlineKeyboardMarkup, Update


class MessageReply:
    @staticmethod
    async def with_update(
        update: Update, text: str = "", keyboard: Optional[InlineKeyboardMarkup] = None
    ):
        if update.effective_sender:
            if keyboard:
                await update.effective_sender.send_message(
                    text=text, reply_markup=keyboard
                )
            else:
                await update.effective_sender.send_message(text=text)
