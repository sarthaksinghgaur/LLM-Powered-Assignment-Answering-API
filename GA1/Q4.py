import re
import math
import numpy as np
import pandas as pd
from typing import Any, List, Union


def execute(question: str, parameter):
    formula = parameter["sheet_formula"]
    result = GA1_QUESTION4(formula)
    return result

def GA1_QUESTION4(formula: str) -> Any:
    """
    Evaluates a Google Sheets formula and returns the result.

    Args:
        formula: A Google Sheets formula string (e.g., "=SUM(A1:A10)", "=ARRAY_CONSTRAIN(SEQUENCE(5), 2, 2)")

    Returns:
        The calculated result of the formula

    Note:
        This is a partial implementation that handles many common functions.
        For full Google Sheets compatibility, you'd need to implement many more functions
        and handle cell references properly.
    """
    # Remove leading = if present
    if formula.startswith('='):
        formula = formula[1:]

    # Parse and evaluate the formula
    try:
        result = _evaluate_expression(formula)
        return result
    except Exception as e:
        return f"#ERROR: {str(e)}"

def _evaluate_expression(expr: str) -> Any:
    """Recursively evaluate an expression"""
    expr = expr.strip()

    # Handle literals
    if expr.upper() == 'TRUE':
        return True
    if expr.upper() == 'FALSE':
        return False
    if expr == '""':
        return ""
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    if re.match(r'^-?\d+$', expr):
        return int(expr)
    if re.match(r'^-?\d*\.\d+$', expr):
        return float(expr)

    # Handle function calls
    if '(' in expr:
        func_name = expr[:expr.index('(')].upper()
        args_str = expr[expr.index('(')+1:expr.rindex(')')]
        args = _parse_arguments(args_str)

        # Evaluate each argument
        evaluated_args = [_evaluate_expression(arg) for arg in args]

        # Call the appropriate function
        if func_name in _FUNCTION_MAP:
            return _FUNCTION_MAP[func_name](*evaluated_args)
        else:
            raise NotImplementedError(f"Function {func_name} not implemented")

    # Handle cell references (simplified - just return the reference as string)
    if re.match(r'^[A-Z]+\d+$', expr, re.IGNORECASE):
        return expr

    # Handle simple arithmetic
    if '+' in expr:
        parts = expr.split('+', 1)
        return _evaluate_expression(parts[0]) + _evaluate_expression(parts[1])
    if '-' in expr and not expr.startswith('-'):
        parts = expr.split('-', 1)
        return _evaluate_expression(parts[0]) - _evaluate_expression(parts[1])
    if '*' in expr:
        parts = expr.split('*', 1)
        return _evaluate_expression(parts[0]) * _evaluate_expression(parts[1])
    if '/' in expr:
        parts = expr.split('/', 1)
        return _evaluate_expression(parts[0]) / _evaluate_expression(parts[1])

    # If we get here, we don't know how to evaluate the expression
    raise ValueError(f"Could not evaluate expression: {expr}")

def _parse_arguments(args_str: str) -> List[str]:
    """Parse function arguments, handling nested parentheses and quoted strings"""
    args = []
    current = []
    paren_level = 0
    in_quotes = False
    escape = False

    for char in args_str:
        if escape:
            current.append(char)
            escape = False
        elif char == '\\':
            escape = True
        elif char == '"' and not in_quotes:
            in_quotes = True
            current.append(char)
        elif char == '"' and in_quotes:
            in_quotes = False
            current.append(char)
        elif char == '(' and not in_quotes:
            paren_level += 1
            current.append(char)
        elif char == ')' and not in_quotes:
            paren_level -= 1
            current.append(char)
        elif char == ',' and not in_quotes and paren_level == 0:
            args.append(''.join(current).strip())
            current = []
        else:
            current.append(char)

    if current:
        args.append(''.join(current).strip())

    return args

# Function implementations
def _sum(*args: Any) -> Union[int, float]:
    """Implementation of SUM function"""
    flat_args = _flatten_args(args)
    return sum(arg for arg in flat_args if isinstance(arg, (int, float)))

def _sequence(rows: int, cols: int = 1, start: int = 1, step: int = 1) -> List[List[int]]:
    """Implementation of SEQUENCE function"""
    result = []
    value = start
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(value)
            value += step
        result.append(row)
    return result

def _array_constrain(array: List[List[Any]], rows: int, cols: int) -> List[List[Any]]:
    """Implementation of ARRAY_CONSTRAIN function"""
    if not isinstance(array, list) or not all(isinstance(row, list) for row in array):
        array = [[array]]

    constrained = []
    for i in range(min(rows, len(array))):
        row = array[i]
        constrained_row = row[:min(cols, len(row))]
        # Pad with None if needed
        while len(constrained_row) < cols:
            constrained_row.append(None)
        constrained.append(constrained_row)

    # Pad with empty rows if needed
    while len(constrained) < rows:
        constrained.append([None] * cols)

    return constrained

def _flatten_args(args: Any) -> List[Any]:
    """Flatten nested lists/tuples into a single list"""
    flat = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            flat.extend(_flatten_args(arg))
        else:
            flat.append(arg)
    return flat

# Map of supported functions
_FUNCTION_MAP = {
    'SUM': _sum,
    'SEQUENCE': _sequence,
    'ARRAY_CONSTRAIN': _array_constrain,
    # Add more functions here as needed
}