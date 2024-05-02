from __future__ import annotations
import importlib
from src.actions.utility.bot_name_mapper import BotModulePathMapper
from src.helpers.cli.arg_helper import ArgHelper
from src.types.arg_data import ArgData


class AppMediator:
    def read_args(self) -> AppMediator:
        self.arg_data = ArgData.from_dict(
            ArgHelper(["bot_id", "bot_number"])
            .check_help()
            .check_args()
            .must_include("bot_id", "bot_number")
            .get_data()
        )
        return self

    def read_configs(self) -> AppMediator:
        return self

    def run_bot(self) -> None:
        bot_number = self.arg_data.bot_number
        bot_name = BotModulePathMapper.map(bot_number)
        bot_module = importlib.import_module(bot_name)
        bot_module.main(bot_id=self.arg_data.bot_id)
