"""COPYRIGHT © 2022 Exenifix
A module for evaluating simple math expressions without eval(). Licensed under MIT license (see LICENSE for details)."""


from .tokenization import tokenize
from .evaluation import build_evaluation_tree
from .errors import *


def evaluate(expr: str) -> int | float:
    """
    Evaluates the expression and returns its result. Raises one of ``InvalidExpression``'s derivatives on
    parsing failure.

    :param expr: The expression to evaluate.
    :type expr: str
    :raise InvalidExpression: expression parsing failed.
    :raise UnexpectedToken: got something at wrong position (eg. in "(2 + 3) .3"" the . is unexpected).
    :raise InvalidToken: got neither a number nor an operator.
    :raise BracesMismatch: some braces are not paired.
    :raise InvalidOperator: got non-existent operator (eg. in "(2 += 3) * 60" the += is non-existent)
    :return: The result of the expression.
    """
    return build_evaluation_tree(tokenize(expr)).evaluate()
