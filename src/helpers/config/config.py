from dataclasses import dataclass, field
from typing import Any, List
from pylib_0xe.config.config import File, JsonHelper, PathHelper


@dataclass
class Config:
    file_path: str = __file__
    base_folder: str = "configs"  # separate nested folders by dot
    root_name: str = "src"
    file_format: str = ".json"

    def read(self, selector: str, **kwargs) -> Any:
        index = selector.find(".")
        if index < 0:
            file_name = selector
            selector = ""
        else:
            file_name = selector[:index]
            selector = selector[index + 1 :]
        return self.get(file_name, selector, **kwargs)

    def get(self, file_name: str, selector: str, default: Any = None) -> Any:
        json = File.read_json(
            PathHelper.from_root(
                self.file_path,
                *self.base_folder.split("."),
                file_name + self.file_format,
                root_name=self.root_name
            )
        )
        value = JsonHelper.selector_get_value(json, selector)
        if value != {}:
            return value
        return default
