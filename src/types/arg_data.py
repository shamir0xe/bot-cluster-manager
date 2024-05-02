from dataclasses import dataclass
from typing import Any
from pylib_0xe.data.data_transfer_object import DataTransferObject


@dataclass
class ArgData(DataTransferObject):
    bot_id: int = -1
    bot_number: int = -1

    @staticmethod
    def bot_id_mapper(bot_id: Any) -> int:
        return int(bot_id)

    @staticmethod
    def bot_number_mapper(bot_number: Any) -> int:
        return int(bot_number)
