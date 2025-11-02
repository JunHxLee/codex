"""Dice parsing and rolling helpers for Dungeons & Dragons 5e.

The goal of the module is to make dice expressions such as ``2d6+3`` or
``d20-1`` simple to parse and evaluate from Python.  The implementation is
lightweight but includes a couple of conveniences often required by bot
or rules engine authors:

* ``parse_expression`` converts a dice expression into structured terms
  that can be evaluated or inspected.
* ``roll`` evaluates an expression and returns both the total and the
  individual die results.
* ``expected_value`` returns the average result of a dice expression –
  useful for statistical tooling.
* ``roll_d20``/``roll_with_advantage``/``roll_with_disadvantage`` provide
  ergonomic wrappers for the most common d20 mechanics.

The functions only depend on Python's :mod:`random` module, so callers can
inject their own RNG (for example a deterministic :class:`random.Random`
for testing) via the ``rng`` parameter.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import List, NamedTuple, Optional, Tuple

__all__ = [
    "DiceTerm",
    "ModifierTerm",
    "DiceExpression",
    "parse_expression",
    "roll",
    "expected_value",
    "roll_d20",
    "roll_with_advantage",
    "roll_with_disadvantage",
]

_TOKEN_RE = re.compile(r"[+-]?[^+-]+")


@dataclass(frozen=True)
class DiceTerm:
    """A single dice term such as ``2d6``.

    ``count`` indicates how many dice are rolled, ``size`` the number of
    faces, and ``sign`` whether the term is added or subtracted.
    """

    count: int
    size: int
    sign: int = 1

    def __post_init__(self) -> None:  # pragma: no cover - dataclass hook
        if self.count < 0:
            raise ValueError("Dice count must be non-negative")
        if self.size <= 0:
            raise ValueError("Die size must be positive")
        if self.sign not in (1, -1):
            raise ValueError("Sign must be 1 or -1")


@dataclass(frozen=True)
class ModifierTerm:
    """A numeric modifier term such as ``+3`` or ``-2``."""

    value: int


class DiceExpression(NamedTuple):
    """Structured representation of a parsed dice expression."""

    dice: Tuple[DiceTerm, ...]
    modifiers: Tuple[ModifierTerm, ...]

    @property
    def modifier_total(self) -> int:
        """Return the sum of all modifiers in the expression."""

        return sum(m.value for m in self.modifiers)


def _parse_token(token: str) -> Tuple[Optional[DiceTerm], Optional[ModifierTerm]]:
    original = token
    token = token.strip()
    if not token:
        raise ValueError("Empty token in dice expression")

    sign = 1
    if token[0] == "+":
        token = token[1:]
    elif token[0] == "-":
        sign = -1
        token = token[1:]

    if "d" in token.lower():
        count_part, size_part = token.lower().split("d", 1)
        count = int(count_part) if count_part else 1
        size = int(size_part)
        return DiceTerm(count=count, size=size, sign=sign), None

    # Otherwise treat as a flat modifier.
    if not token:
        raise ValueError(f"Invalid modifier in token: {original!r}")
    value = int(token) * sign
    return None, ModifierTerm(value=value)


def parse_expression(expr: str) -> DiceExpression:
    """Parse ``expr`` into a :class:`DiceExpression`.

    Whitespace is ignored and uppercase ``D`` is treated the same as
    lowercase.  Expressions must consist of dice terms (``NdM``) and
    integer modifiers combined with ``+`` or ``-`` signs.  Parentheses or
    multiplication are intentionally not supported to keep the parser
    small and predictable.
    """

    expr = expr.replace(" ", "")
    if not expr:
        raise ValueError("Dice expression cannot be empty")

    dice_terms: List[DiceTerm] = []
    modifiers: List[ModifierTerm] = []
    for token in _TOKEN_RE.findall(expr):
        dice, modifier = _parse_token(token)
        if dice:
            dice_terms.append(dice)
        elif modifier:
            modifiers.append(modifier)
    if not dice_terms and not modifiers:
        raise ValueError(f"Could not parse expression: {expr!r}")
    return DiceExpression(tuple(dice_terms), tuple(modifiers))


class DiceRollResult(NamedTuple):
    """Result returned by :func:`roll`."""

    total: int
    dice_results: Tuple[Tuple[int, ...], ...]
    modifiers: Tuple[int, ...]

    def detail(self) -> str:
        """Return a human-readable summary of the roll."""

        dice_parts = [f"{tuple_vals}" for tuple_vals in self.dice_results]
        modifier_total = sum(self.modifiers)
        modifier_str = f" {modifier_total:+d}" if modifier_total else ""
        return f"{' + '.join(dice_parts)}{modifier_str} = {self.total}"


def roll(expr: str, *, rng: Optional[random.Random] = None) -> DiceRollResult:
    """Roll ``expr`` and return the total along with per-die results."""

    parsed = parse_expression(expr)
    rng = rng or random.Random()

    dice_results: List[Tuple[int, ...]] = []
    total = parsed.modifier_total

    for term in parsed.dice:
        if term.count == 0:
            dice_results.append(tuple())
            continue
        rolls = tuple(rng.randint(1, term.size) for _ in range(term.count))
        subtotal = sum(rolls) * term.sign
        dice_results.append(rolls if term.sign > 0 else tuple(-r for r in rolls))
        total += subtotal

    modifiers = tuple(m.value for m in parsed.modifiers)
    return DiceRollResult(total=total, dice_results=tuple(dice_results), modifiers=modifiers)


def expected_value(expr: str) -> float:
    """Return the mathematical expected value of ``expr``."""

    parsed = parse_expression(expr)
    expected = parsed.modifier_total
    for term in parsed.dice:
        # Average of a die is (n + 1) / 2.
        expected += term.sign * term.count * (term.size + 1) / 2
    return expected


def _ensure_rng(rng: Optional[random.Random]) -> random.Random:
    return rng or random.Random()


def roll_d20(*, rng: Optional[random.Random] = None) -> int:
    """Roll a single d20."""

    rng = _ensure_rng(rng)
    return rng.randint(1, 20)


def roll_with_advantage(*, rng: Optional[random.Random] = None) -> Tuple[int, Tuple[int, int]]:
    """Roll ``2d20`` and keep the highest result."""

    rng = _ensure_rng(rng)
    first = rng.randint(1, 20)
    second = rng.randint(1, 20)
    return max(first, second), (first, second)


def roll_with_disadvantage(*, rng: Optional[random.Random] = None) -> Tuple[int, Tuple[int, int]]:
    """Roll ``2d20`` and keep the lowest result."""

    rng = _ensure_rng(rng)
    first = rng.randint(1, 20)
    second = rng.randint(1, 20)
    return min(first, second), (first, second)


DiceRoll = DiceRollResult  # Backwards compatibility alias.
