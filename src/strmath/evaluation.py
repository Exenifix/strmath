from typing import TypeVar

from .types import Number, Tokenized, Operator

T_ETN = TypeVar("T_ETN", bound="EvaluationTreeNode")


class EvaluationTreeNode:
    def __init__(self, a: Number | T_ETN, op: "Operator", b: Number | T_ETN):
        self.a = a
        self.op = op
        self.b = b

    def evaluate(self) -> Number:
        if isinstance(self.a, EvaluationTreeNode):
            self.a = self.a.evaluate()
        if isinstance(self.b, EvaluationTreeNode):
            self.b = self.b.evaluate()
        return self.op.evaluate(self.a, self.b)


def build_evaluation_tree(
    tokenized_expr: Tokenized | Number,
) -> EvaluationTreeNode | Number:
    """
    If the tokenized expression is a number, returns it; if it's a singleton, evaluates it; if it's a triple, builds
    a node with the first element as the left child, the second element as the operator, and the third element as the
    right child; otherwise, build a node with the first element as the left child, the second element as the operator,
    and the rest of the elements as the right child.

    :param tokenized_expr: The tokenized expression to build the evaluation tree from
    :type tokenized_expr: Tokenized | Number
    :return: an evaluation tree.
    """
    if isinstance(tokenized_expr, Number):
        return tokenized_expr
    if len(tokenized_expr) == 1:
        return build_evaluation_tree(tokenized_expr[0])
    if len(tokenized_expr) == 3:
        return EvaluationTreeNode(
            build_evaluation_tree(tokenized_expr[0]),
            tokenized_expr[1],
            build_evaluation_tree(tokenized_expr[2]),
        )

    return EvaluationTreeNode(
        build_evaluation_tree(tokenized_expr[0]),
        tokenized_expr[1],
        build_evaluation_tree(tokenized_expr[2:]),
    )
