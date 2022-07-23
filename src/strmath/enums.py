from enum import Enum


class TokenType(Enum):
    NUMBER = 0
    OPERATOR = 1
    EXPRESSION = 2
    DOT = 3
    FLOAT = 4
