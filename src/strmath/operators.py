from .errors import InvalidOperator

Number = int | float


class Operator:
    def __init__(self, op: str):
        self.op = op

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.op

    def evaluate(self, a: Number, b: Number) -> Number:
        match self.op:
            case "+":
                return a + b
            case "-":
                return a - b
            case "/":
                return a / b
            case "*":
                return a * b
            case "%":
                return a % b
            case "**":
                return a**b
            case "//":
                return a // b
        raise InvalidOperator(self.op)
