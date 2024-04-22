from enum import Enum


class OperandTypes(Enum):
    GREATER_EQ = ">="
    GREATER = ">"
    LESSER_EQ = "<="
    LESSER = "<"
    EQUAL = "=="
    NOT_EQUAL = "!="
