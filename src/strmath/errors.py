class InvalidExpression(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidToken(InvalidExpression):
    def __init__(self, token: str):
        super().__init__("Token `%s` is not a number nor an operator." % token)


class BracesMismatch(InvalidExpression):
    def __init__(self):
        super().__init__("Some braces are not paired")


class InvalidOperator(InvalidExpression):
    def __init__(self, op: str):
        super().__init__("`%s` is not a valid operator" % op)


class UnexpectedToken(InvalidExpression):
    def __init__(self, token: str):
        super().__init__("Got an unexpected token `%s`" % token)
