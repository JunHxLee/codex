"""Ability score helpers for Dungeons & Dragons 5e."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, Mapping, Tuple

ABILITY_NAMES: Tuple[str, ...] = (
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
)

__all__ = ["ABILITY_NAMES", "modifier", "AbilityScores", "validate_score"]


def validate_score(score: int) -> int:
    """Validate and normalise an ability score.

    The function follows the 5e Player's Handbook: natural scores range
    from 1–20 for player characters, while 30 is the absolute maximum for
    creatures.  The value is returned unchanged if it falls within the
    allowed range.
    """

    if not 1 <= score <= 30:
        raise ValueError("Ability scores must be between 1 and 30")
    return score


def modifier(score: int) -> int:
    """Return the ability modifier for ``score``."""

    return (validate_score(score) - 10) // 2


@dataclass(frozen=True)
class AbilityScores:
    """Container for the six standard D&D ability scores."""

    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    def __post_init__(self) -> None:  # pragma: no cover - dataclass hook
        for ability in ABILITY_NAMES:
            validate_score(getattr(self, ability))

    def modifier(self, ability: str) -> int:
        """Return the modifier for ``ability`` (case-insensitive)."""

        key = ability.lower()
        if key not in ABILITY_NAMES:
            raise KeyError(f"Unknown ability: {ability!r}")
        return modifier(getattr(self, key))

    def to_dict(self) -> Dict[str, int]:
        """Return a mutable dictionary copy of the scores."""

        return {ability: getattr(self, ability) for ability in ABILITY_NAMES}

    @classmethod
    def from_mapping(cls, scores: Mapping[str, int]) -> "AbilityScores":
        """Construct :class:`AbilityScores` from a mapping."""

        values = {}
        for ability in ABILITY_NAMES:
            try:
                values[ability] = validate_score(int(scores[ability]))
            except KeyError as exc:  # pragma: no cover - defensive coding
                raise KeyError(f"Missing ability score for {ability!r}") from exc
        return cls(**values)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        for ability in ABILITY_NAMES:
            yield ability, getattr(self, ability)
