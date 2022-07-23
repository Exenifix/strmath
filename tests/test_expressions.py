import os
import time
from random import randint, choice
from typing import Any, Callable

from py_expression_eval import Parser
from mathparse.mathparse import parse
from tabulate import tabulate
from exencolor import Decoration, colored, Color
import InfixParser

from strmath import evaluate

TEST_EXPRESSIONS_AMOUNT = int(os.getenv("TEST_EXPRESSIONS_AMOUNT", 100))
MAX_EXPRESSION_COMPLEXITY = int(os.getenv("MAX_EXPRESSION_COMPLEXITY", 3))
BEST_TIMES_YELLOW = 50
BEST_TIMES_GREEN = 80
FAILURES_YELLOW = 3
FAILURES_RED = 10

FLOAT_ROUND = 5
MAX_RESULT_LENGTH = int(os.getenv("MAX_RESULT_LENGTH", 20))  # parse -1 to disable


def generate_expression(complexity: int) -> str:
    e = str(random_num(1))
    for _ in range(complexity):
        op = choice(["+", "-", "*", "/", "//", "%", "**"])
        # to avoid very huge numbers the power is limited to random number from 2 to 4
        e += f" {op} {random_num(complexity-1) if op != '**' else randint(2, 4)}"
    return e


def random_num(complexity: int) -> str:
    a = randint(0, 1)
    if a or complexity <= 1:
        return str(randint(1, 99))
    else:
        return f"({generate_expression(complexity)})"


def generate_expressions(amount: int, max_complexity: int = 3) -> list[str]:
    return [generate_expression(randint(1, max_complexity)) for _ in range(amount)]


def pee_eval(e: str):
    return Parser().parse(e).evaluate({})


def time_func(func: Callable, *args) -> tuple[float, Any] | tuple[str, str]:
    start = time.time()
    try:
        r = func(*args)
    except:
        return ("FAILURE",) * 2
    return round(time.time() - start, 5), r


def test_expressions():
    names = ["Python", "StrMath", "PEE", "Mathparse", "InfixParser"]
    data = [
        ["No.", "Expression"]
        + [i + " Eval" for i in names]
        + [i + " Eval Time" for i in names]
    ]
    functions_to_test = (eval, evaluate, pee_eval, parse, InfixParser.evaluate)
    failures: list[int | str] = [0] * len(functions_to_test)
    best_times: list[int | str] = [0] * len(functions_to_test)
    print()
    expressions = generate_expressions(TEST_EXPRESSIONS_AMOUNT, MAX_EXPRESSION_COMPLEXITY)
    amount = len(expressions)
    for num, expr in enumerate(expressions, 1):
        results = []
        times = []
        failure = False
        for fc in functions_to_test:
            eval_time, result = time_func(fc, expr)
            if fc == eval and eval_time == "FAILURE":
                failure = True
                break
            results.append(
                round(result, FLOAT_ROUND) if result != "FAILURE" else result
            )
            times.append(eval_time)
        if failure:
            colored_results, colored_times = (
                (colored("SKIPPED", foreground=Color.BRIGHT_YELLOW),)
                * len(functions_to_test),
            ) * 2
            amount -= 1
        else:
            expected_value = results[0]
            colored_results = []
            for i, res in enumerate(results):
                if res == expected_value:
                    color = Color.BRIGHT_GREEN
                else:
                    color = Color.BRIGHT_RED
                    failures[i] += 1
                res = str(res)
                if -1 < MAX_RESULT_LENGTH < len(res):
                    res = res[:MAX_RESULT_LENGTH] + "..."
                colored_results.append(colored(res, foreground=color))

            min_time = min([t for t in times if isinstance(t, (float, int))], default=1)
            colored_times = []
            for i, res in enumerate(times):
                if res == "FAILURE":
                    color = Color.BRIGHT_RED
                elif res == min_time:
                    best_times[i] += 1
                    color = Color.BRIGHT_GREEN
                else:
                    color = Color.BRIGHT_YELLOW
                colored_times.append(colored(res, foreground=color))

        d = [num, expr]
        d.extend(colored_results)
        d.extend(colored_times)
        data.append(d)

    print("EXPRESSIONS".center(195, "-"))
    print(
        tabulate(
            data,
            headers="firstrow",
            tablefmt="pretty",
            numalign="left",
            stralign="left",
        )
    )

    failures_percents = [int(i / amount * 100) for i in failures]
    best_times_percents = [int(i / amount * 100) for i in best_times]
    colored_failures = []
    colored_failures_percents = []
    for i, v in enumerate(failures_percents):
        if v >= FAILURES_RED:
            color = Color.BRIGHT_RED
        elif v >= FAILURES_YELLOW:
            color = Color.BRIGHT_YELLOW
        else:
            color = Color.BRIGHT_GREEN
        colored_failures.append(colored(failures[i], foreground=color))
        colored_failures_percents.append(
            colored(str(failures_percents[i]) + "%", foreground=color)
        )
    colored_best_times = []
    colored_best_times_percents = []
    for i, v in enumerate(best_times_percents):
        if v < BEST_TIMES_YELLOW:
            color = Color.BRIGHT_RED
        elif v < BEST_TIMES_GREEN:
            color = Color.BRIGHT_YELLOW
        else:
            color = Color.BRIGHT_GREEN
        colored_best_times.append(colored(best_times[i], foreground=color))
        colored_best_times_percents.append(
            colored(str(best_times_percents[i]) + "%", foreground=color)
        )

    print()
    print("SUMMARY".center(195, "-"))
    print(
        tabulate(
            [
                ["Failures"] + colored_failures,
                ["Failures (%)"] + colored_failures_percents,
                ["Best Times"] + colored_best_times,
                ["Best Times (%)"] + colored_best_times_percents,
            ],
            [""] + names,
            tablefmt="pretty",
            stralign="left",
            numalign="left",
        )
    )
    if amount != len(expressions):
        print(
            colored(
                len(expressions) - amount,
                foreground=Color.BRIGHT_YELLOW,
                decoration=Decoration.BOLD,
            )
            + colored(
                " samples were skipped due to bad expression generation.",
                foreground=Color.BRIGHT_YELLOW,
            )
        )

    assert failures_percents[1] < FAILURES_YELLOW
    assert best_times_percents[1] > BEST_TIMES_GREEN
