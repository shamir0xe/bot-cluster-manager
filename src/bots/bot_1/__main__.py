from __future__ import annotations
import asyncio
import telegram
from src.helpers.config.bot_config import BotConfig
from src.types.bot_env_data import BotEnvData


class Bot_1:
    env: BotEnvData
    bot: telegram.Bot

    def read_environments(self) -> Bot_1:
        self.env = BotEnvData.from_dict(BotConfig(__file__).read("env"))
        return self

    def read_configs(self) -> Bot_1:
        return self

    def run(self) -> None:
        asyncio.run(self.main_procedure())

    async def main_procedure(self):
        self.bot = telegram.Bot(self.env.token)
        async with self.bot:
            print(await self.bot.get_me())
            updates = await self.bot.get_updates()
            for update_instance in updates:
                print(update_instance)
                if (
                    update_instance.message is not None
                    and update_instance.message.from_user is not None
                ):
                    await self.bot.send_message(
                        text=f"Hi {update_instance.message.from_user.full_name}",
                        chat_id=update_instance.message.chat.id,
                    )


def main():
    Bot_1().read_configs().read_environments().run()

