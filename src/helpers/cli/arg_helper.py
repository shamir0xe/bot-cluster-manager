from __future__ import annotations
from dataclasses import dataclass, field
from pylib_0xe.argument.argument_parser import ArgumentParser


@dataclass
class ArgHelper:
    attributes: list[str]
    data: dict[str, str] = field(default_factory=dict)
    prefix: str = "--"

    def show_valid_options(self) -> str:
        return f"available options are: {self.attributes}"

    def done(self, message: str = ""):
        print(message)
        exit(0)

    def check_help(self, help_keyword="help") -> ArgHelper:
        for key, _ in ArgumentParser.get_options(option_prefix=self.prefix).items():
            key = key.lower()
            if key == help_keyword:
                self.done(self.show_valid_options())
        return self

    def check_args(self, skipps: list[str] = []) -> ArgHelper:
        for key, value in ArgumentParser.get_options(option_prefix=self.prefix).items():
            key = key.lower()
            if key in skipps:
                continue
            if key not in self.attributes:
                self.done(f"Error: available options are: {self.attributes}")
            if value == "":
                continue
            self.data[key] = value
        return self

    def must_include(self, *args) -> ArgHelper:
        for arg in args:
            if not ArgumentParser.is_option(arg) or self.data[arg] == "":
                self.done(f"Error: set the {self.prefix}{arg}")
        return self

    def get_data(self) -> dict:
        return self.data
