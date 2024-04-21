from __future__ import annotations
from typing import List
import importlib

from src.actions.variable_module_path_mapper import VariableModulePathMapper
from src.helpers.config.config import Config
from src.types.variable import Variable


class VariableMediator:
    variables: List[Variable]

    def read_config(self) -> VariableMediator:
        self.var_names = Config().read("variables.available_vars")
        return self

    def register_variables(self) -> VariableMediator:
        self.variables = []
        for var_name in self.var_names:
            path, class_name = VariableModulePathMapper.map(var_name)
            module = importlib.import_module(path)
            variable_class = getattr(module, class_name)
            var = variable_class()
            self.variables.append(var)
        return self

    def get_variables(self) -> List[Variable]:
        return self.variables
