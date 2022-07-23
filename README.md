# strmath

![tests](.github/workflows/test.yml/badge.svg)
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
As [tests](link not added) <!-- TODO add link --> show, the library is 100% accurate with python native evaluation:
```
+----------------+--------+---------+-----+-----------+-------------+
|                | Python | StrMath | PEE | Mathparse | InfixParser |
+----------------+--------+---------+-----+-----------+-------------+
| Failures       | 0      | 0       | 61  | 150       | 91          |
| Failures (%)   | 0%     | 0%      | 30% | 75%       | 45%         |
| Best Times     | 198    | 190     | 126 | 65        | 159         |
| Best Times (%) | 100%   | 95%     | 63% | 32%       | 80%         |
+----------------+--------+---------+-----+-----------+-------------+
```
In the test above, 198 randomly generated samples were submitted to Python `eval()` and several other parsing libraries, including `strmath`. 
As you can see, the library has 0 failures and almost same speed with native python. You can see test implementation [here](tests/test_expressions.py).

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
This repository is licensed under MIT license. See [LICENSE](LICENSE) for details.
