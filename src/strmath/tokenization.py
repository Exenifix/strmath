import re

from .enums import TokenType
from .errors import BracesMismatch, InvalidToken, UnexpectedToken
from .types import Number, Tokenized
from .operators import Operator


OPERATORS = ["+", "-", "/", "//", "*", "%", "**", "//"]
OPERATORS_ORDER = [["**"], ["*", "/", "//", "%"], ["+", "-"]]

FLOAT_REGEX = re.compile(r"\d+\.\d+")


def get_token_type(token: str) -> TokenType:
    if token == ".":
        return TokenType.DOT
    if token.isnumeric():
        return TokenType.NUMBER
    if token in OPERATORS:
        return TokenType.OPERATOR
    if re.match(FLOAT_REGEX, token) is not None:
        return TokenType.FLOAT

    raise InvalidToken(token)


def convert_token(token: str | list) -> Number | Operator | Tokenized:
    if isinstance(token, list):
        return token
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
    for s in expr:
        if s == "(":
            braces += 1
            if not gathering_expression:
                gathering_expression = True
                cached_token_type = TokenType.EXPRESSION
                if cached_token != "":
                    tokenized.append(cached_token)
                cached_token = ""
        elif s == ")":
            braces -= 1

        if braces > 0:
            cached_token += s
            continue
        if braces < 0:
            raise BracesMismatch()

        if braces == 0 and gathering_expression:
            tokenized.append(tokenize(cached_token[1:]))
            gathering_expression = False
            cached_token = ""
            continue

        token_type = get_token_type(s)
        if (token_type == TokenType.DOT and cached_token_type != TokenType.NUMBER) or (
            cached_token_type == TokenType.EXPRESSION
            and token_type != TokenType.OPERATOR
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
            if cached_token_type != TokenType.EXPRESSION:
                validate_token(cached_token)  # to avoid double operators
                tokenized.append(cached_token)
            cached_token = s
        cached_token_type = token_type

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
                    return [apply_order(expr[:i]), item, apply_order(expr[i+1:])]
