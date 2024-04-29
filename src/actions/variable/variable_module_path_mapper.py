from typing import Tuple
from pylib_0xe.string.string_helper import StringHelper
from src.helpers.config.config import Config


class VariableModulePathMapper:
    @staticmethod
    def map(var_name: str) -> Tuple[str, str]:
        var_name += "_variable"
        camel_case = StringHelper.snake_to_camel(var_name, True)
        return Config().read("variables.path").format(var_name), camel_case
