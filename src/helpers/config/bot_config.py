import os
from dataclasses import dataclass
from typing import Any

from pylib_0xe.config.config import File
from pylib_0xe.json.json_helper import JsonHelper


@dataclass
class BotConfig:
    file_path: str
    folder_name: str = "configs"

    def get(self, filename: str, selector: str, default: Any = None) -> Any:
        home_path = os.path.normpath(os.path.abspath(os.sep))
        path = os.path.dirname(self.file_path)
        found = False
        json = {}
        while not found:
            try:
                json = File.read_json(
                    os.path.join(path, self.folder_name, f"{filename}.json")
                )
                found = True
            except Exception:
                path = os.path.normpath(os.path.join(path, ".."))
                if path == home_path:
                    raise Exception("No such config exists")
        value = JsonHelper.selector_get_value(json, selector)
        if value != {}:
            return value
        return default

    def read(self, selector: str) -> Any:
        index = selector.find(".")
        if index < 0:
            filename = selector
            selector = ""
        else:
            filename = selector[:index]
            selector = selector[index + 1 :]
        return self.get(filename, selector)
