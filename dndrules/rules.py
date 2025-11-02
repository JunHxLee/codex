"""Convenience helpers that combine dice rolling with modifiers."""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional, Tuple

from . import dice

AdvantageState = str

__all__ = [
    "AdvantageState",
    "CheckResult",
    "ContestResult",
    "resolve_check",
    "resolve_contest",
]


@dataclass(frozen=True)
class CheckResult:
    """Container describing the outcome of a single check."""

    total: int
    modifier: int
    dc: int
    success: bool
    natural: int
    roll_details: Tuple[int, ...]


@dataclass(frozen=True)
class ContestResult:
    """Outcome of a contest between two checks."""

    total_a: int
    total_b: int
    winner: Optional[str]
    check_a: CheckResult
    check_b: CheckResult

    @property
    def is_tie(self) -> bool:
        return self.winner is None


def _roll_d20(state: AdvantageState, *, rng: Optional[random.Random]) -> Tuple[int, Tuple[int, ...]]:
    state = state.lower()
    if state == "normal":
        value = dice.roll_d20(rng=rng)
        return value, (value,)
    if state == "advantage":
        value, detail = dice.roll_with_advantage(rng=rng)
        return value, detail
    if state == "disadvantage":
        value, detail = dice.roll_with_disadvantage(rng=rng)
        return value, detail
    raise ValueError("Advantage state must be 'normal', 'advantage' or 'disadvantage'")


def resolve_check(
    modifier: int,
    dc: int,
    *,
    advantage: AdvantageState = "normal",
    rng: Optional[random.Random] = None,
) -> CheckResult:
    """Roll a d20 check with ``modifier`` against ``dc``."""

    rng = rng or random.Random()
    natural, detail = _roll_d20(advantage, rng=rng)
    total = natural + modifier
    return CheckResult(
        total=total,
        modifier=modifier,
        dc=dc,
        success=total >= dc,
        natural=natural,
        roll_details=detail,
    )


def resolve_contest(
    modifier_a: int,
    modifier_b: int,
    *,
    advantage_a: AdvantageState = "normal",
    advantage_b: AdvantageState = "normal",
    rng: Optional[random.Random] = None,
) -> ContestResult:
    """Resolve a contest between two opponents.

    The checks use a shared RNG to avoid subtly favouring one contestant
    over the other in deterministic contexts (useful for testing).
    """

    rng = rng or random.Random()
    check_a = resolve_check(modifier_a, 0, advantage=advantage_a, rng=rng)
    check_b = resolve_check(modifier_b, 0, advantage=advantage_b, rng=rng)

    total_a = check_a.total
    total_b = check_b.total
    winner: Optional[str]
    if total_a > total_b:
        winner = "a"
    elif total_b > total_a:
        winner = "b"
    else:
        winner = None

    return ContestResult(
        total_a=total_a,
        total_b=total_b,
        winner=winner,
        check_a=check_a,
        check_b=check_b,
    )
