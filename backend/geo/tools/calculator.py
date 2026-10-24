"""``calculate`` tool: exact arithmetic done by code, not by the model (Buổi 4 rule).

Only numbers, + - * / ** %, unary minus and parentheses are accepted. The expression is parsed
with ``ast`` and evaluated node by node; nothing is ever passed to ``eval``.
"""

from __future__ import annotations

import ast
import operator
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from geo.harness.contract import error, ok
from geo.tools.registry import ToolSpec

MAX_EXPRESSION_LENGTH = 200
MAX_POWER = 100

_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}


class CalculateArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expression: str = Field(
        description="Arithmetic expression with plain numbers, e.g. 2400000*30*0.015. "
        "Use '.' as decimal point and no thousands separators."
    )


def _eval(node: ast.AST) -> Decimal:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int | float)
        and not isinstance(node.value, bool)
    ):
        return Decimal(str(node.value))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_POWER:
            raise ValueError(f"exponent larger than {MAX_POWER}")
        return _BINARY[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    raise ValueError(f"unsupported element: {type(node).__name__}")


def format_vi(value: Decimal) -> str:
    """Vietnamese notation: thousands with '.', decimals with ','."""
    rounded = value.quantize(Decimal("0.01")).normalize()
    text = f"{rounded:,f}"
    integer, _, frac = text.partition(".")
    integer = integer.replace(",", ".")
    return f"{integer},{frac}" if frac else integer


def calculate(expression: str) -> dict[str, Any]:
    if len(expression) > MAX_EXPRESSION_LENGTH:
        return error("expression_too_long", f"Keep the expression under {MAX_EXPRESSION_LENGTH} characters")
    try:
        value = _eval(ast.parse(expression, mode="eval"))
    except ZeroDivisionError:
        return error("division_by_zero", "The expression divides by zero")
    except (SyntaxError, ValueError, ArithmeticError) as exc:
        return error("invalid_expression", f"Only numbers and + - * / ** % ( ) are allowed: {exc}")
    return ok(expression=expression, result=float(value), result_vi=format_vi(value))


CALCULATE = ToolSpec(
    name="calculate",
    description=(
        "Evaluate an arithmetic expression exactly. Use it for EVERY computation instead of "
        "computing in your head. Returns result (number) and result_vi (Vietnamese notation)."
    ),
    args_schema=CalculateArgs,
    func=calculate,
)
