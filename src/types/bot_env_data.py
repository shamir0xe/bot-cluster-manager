from pylib_0xe.data.data_transfer_object import DataTransferObject
from dataclasses import dataclass


@dataclass
class BotEnvData(DataTransferObject):
    token: str = ""
