import inspect
import math
import re

from .enums import TokenType
from .errors import (
    BracesMismatch,
    IncompleteFunction,
    InvalidFunction,
    InvalidToken,
    UnexpectedToken,
)
from .evaluation import Function
from .operators import Operator
from .types import Number, Tokenized

UNSUPPORTED_FUNCTIONS = ["dist", "prod", "isclose"]
_supported_functions = [
    i[1]
    for i in inspect.getmembers(
        math,
        lambda x: inspect.isbuiltin(x)
        and callable(x)
        and not x.__name__.startswith("_")
        and x.__name__ not in UNSUPPORTED_FUNCTIONS,
    )
] + [abs, int, float, round, pow]
SUPPORTED_FUNCTIONS = {i.__name__: i for i in _supported_functions}
OPERATORS = ["+", "-", "/", "//", "*", "%", "**", "//"]
OPERATORS_ORDER = [["**"], ["*", "/", "//", "%"], ["+", "-"]]

FLOAT_REGEX = re.compile(r"\d+\.\d+")
FUNCTION_REGEX = re.compile(r"\w{2,10}\(.+\)")


def get_token_type(token: str) -> TokenType:
    if token == ".":
        return TokenType.DOT
    if token.isnumeric():
        return TokenType.NUMBER
    if token in OPERATORS:
        return TokenType.OPERATOR
    if re.match(FLOAT_REGEX, token) is not None:
        return TokenType.FLOAT
    if any(f.startswith(token) for f in SUPPORTED_FUNCTIONS):
        return TokenType.FUNCTION

    raise InvalidToken(token)


def convert_token(token: str | list) -> Number | Operator | Function | Tokenized:
    if isinstance(token, list):
        return token
    elif re.match(FUNCTION_REGEX, token) is not None:
        name = token.split("(", 1)[0]
        try:
            func = SUPPORTED_FUNCTIONS[name]
        except KeyError:
            raise InvalidFunction(name) from None
        args = token.replace(name, "", 1)[1:-1].split(",")
        return Function(func, *(tokenize(arg) for arg in args))
    else:
        token_type = get_token_type(token)
        if token_type == TokenType.NUMBER:
            return int(token)
        if token_type == TokenType.OPERATOR:
            return Operator(token)
        if token_type == TokenType.FLOAT:
            return float(token)
        raise InvalidToken(token)


def validate_token(token: str):
    try:
        get_token_type(token)
    except InvalidToken as e:
        raise e from None


def tokenize(expr: str) -> Tokenized:
    expr = expr.replace(" ", "").strip()
    tokenized = []
    cached_token: str | list[str, list] = ""
    cached_token_type: TokenType | None = None
    braces: int = 0
    gathering_expression = False
    gathering_func = False
    gathering_func_args = False
    for s in expr:
        if s == "(":
            braces += 1
            if not gathering_expression and not gathering_func:
                gathering_expression = True
                cached_token_type = TokenType.EXPRESSION
                if cached_token != "":
                    tokenized.append(cached_token)
                cached_token = ""
            elif gathering_func:
                gathering_func_args = True
        elif s == ")":
            braces -= 1

        if braces == 0 and gathering_expression:
            tokenized.append(tokenize(cached_token[1:]))
            gathering_expression = False
            cached_token = ""
            continue

        elif braces == 0 and gathering_func and gathering_func_args:
            tokenized.append(cached_token + s)
            cached_token = ""
            gathering_func = False
            gathering_func_args = False
            continue

        if braces > 0 or gathering_func:
            cached_token += s
            continue
        if braces < 0:
            raise BracesMismatch()

        token_type = get_token_type(s)
        if (
            (token_type == TokenType.DOT and cached_token_type != TokenType.NUMBER)
            or (
                cached_token_type == TokenType.EXPRESSION
                and token_type != TokenType.OPERATOR
            )
            or (
                cached_token_type is not None
                and cached_token_type != TokenType.OPERATOR
                and token_type == TokenType.FUNCTION
                and not gathering_func
            )
        ):
            raise UnexpectedToken(cached_token + s)
        elif (
            token_type == cached_token_type
            or cached_token_type is None
            or (token_type, cached_token_type) == (TokenType.DOT, TokenType.NUMBER)
            or (token_type, cached_token_type) == (TokenType.NUMBER, TokenType.DOT)
        ):
            cached_token += s
        else:
            if cached_token_type != TokenType.EXPRESSION and cached_token != "":
                validate_token(cached_token)  # to avoid double operators
                tokenized.append(cached_token)
            cached_token = s
        if token_type == TokenType.FUNCTION:
            gathering_func = True
        cached_token_type = token_type

    if gathering_func or gathering_func:
        raise IncompleteFunction(cached_token)
    if braces > 0:
        raise BracesMismatch()
    if cached_token != "":
        tokenized.append(cached_token)
    return apply_order([convert_token(t) for t in tokenized])


def apply_order(expr: Tokenized) -> Tokenized | Number:
    if len(expr) == 1:
        return expr[0]
    if len(expr) == 3:
        return expr
    for ops in reversed(OPERATORS_ORDER):
        if ops[0] != "**":
            for i, item in enumerate(reversed(expr)):
                if isinstance(item, Operator) and item.op in ops:
                    return [apply_order(expr[: -i - 1]), item, apply_order(expr[-i:])]
        else:
            for i, item in enumerate(expr):
                if isinstance(item, Operator) and item.op in ops:
                    return [apply_order(expr[:i]), item, apply_order(expr[i + 1 :])]
