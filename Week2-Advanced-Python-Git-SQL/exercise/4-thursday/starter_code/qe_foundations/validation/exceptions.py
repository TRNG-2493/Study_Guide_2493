"""Custom exception for failed data validation  (Tuesday: raising/creating custom exceptions).

TODO (Block 4): turn this stub into a useful exception.

Requirements (check_exercise.py tests them):
  * ValidationFailedError is a subclass of Exception (optionally of your own
    project base error from Tuesday, if you have one).
  * ValidationFailedError(rule, rows) accepts the Rule object and the list of
    violating rows (any rule object with .rule_id, .description and .expect).
  * It exposes the attributes   .rule_id   .description   .rows
  * str(error) is ONE readable line that names the rule and the number of rows,
    for example:
        R-04 failed: duration_ms must be present and not negative (2 violating row(s))
    (For an expectation rule that wanted 1 row but got 0, say how many were
     expected vs. found -- your wording.)
"""


class ValidationFailedError(Exception):
    """TODO: carry rule_id, description and rows; write a helpful message."""
    # TODO: def __init__(self, rule, rows): ...
    pass
