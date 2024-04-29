from pylib_0xe.config.config import Config


class BotModulePathMapper:
    @staticmethod
    def map(bot_id: int) -> str:
        return Config(__file__).read("bots.module_path").format(bot_id)
