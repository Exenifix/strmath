![tests](https://github.com/Exenifix/strmath/actions/workflows/test.yml/badge.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/strmath)
![License](https://img.shields.io/github/license/Exenifix/strmath)
![CodeFactor](https://www.codefactor.io/repository/github/exenifix/strmath/badge)
![GitHub release](https://img.shields.io/github/v/release/Exenifix/strmath?label=version)

# strmath

A module for evaluating math expressions without eval(). Currently the module supports only simple math operations (eg.
multiplication, subtraction, division, %) but in the future there will be functions support.

## Installation
The module is available for installation from PyPI
```shell
$ pip install strmath
```

## Basic Usage
```python
from strmath import evaluate


result = evaluate("(90 + 2) // 4")
print(result)
```

## Accuracy
As [tests](https://github.com/Exenifix/strmath/actions/workflows/test.yml) show, the library is 100% accurate with python native evaluation:
```
+----------------+--------+---------+-----+-----------+-------------+
|                | Python | StrMath | PEE | Mathparse | InfixParser |
+----------------+--------+---------+-----+-----------+-------------+
| Failures       | 0      | 0       | 61  | 150       | 91          |
| Failures (%)   | 0%     | 0%      | 30% | 75%       | 45%         |
+----------------+--------+---------+-----+-----------+-------------+
```
In the test above, 198 randomly generated samples were submitted to Python `eval()` and several other parsing libraries, including `strmath`. 
As you can see, the library has 0 failures and almost same speed with native python. You can see test implementation [here](https://github.com/Exenifix/strmath/blob/master/tests/test_expressions.py).

## Features
### Currently Supported
- basic math operations (+, -, /, //, *, **, %) eg. `"2 + 5 * 2" --> 12`
- float operations
- braces eg. `"(2 + 5) * 2" --> 20`

### Planned for Future
- math functions
- custom functions registration
- correct `-` operator as neg (eg. `50+-30`)

## Principle
1. Tokenize expression (split it into operators and numbers)
2. Apply operations order
3. Build evaluation binary tree
4. Evaluate the tree

## License
This repository is licensed under MIT license. See [LICENSE](https://github.com/Exenifix/strmath/blob/master/LICENSE) for details.
