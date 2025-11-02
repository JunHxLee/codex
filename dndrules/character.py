"""High level character math helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

from .abilities import ABILITY_NAMES, AbilityScores

SKILL_ABILITIES = {
    "acrobatics": "dexterity",
    "animal handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom",
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight of hand": "dexterity",
    "stealth": "dexterity",
    "survival": "wisdom",
}

__all__ = [
    "SKILL_ABILITIES",
    "proficiency_bonus",
    "Character",
]


def proficiency_bonus(level: int) -> int:
    """Return the 5e proficiency bonus for ``level``."""

    if level < 1 or level > 20:
        raise ValueError("Character level must be between 1 and 20")
    # 1-4:+2, 5-8:+3, 9-12:+4, 13-16:+5, 17-20:+6.
    return 2 + (level - 1) // 4


@dataclass
class Character:
    """Minimal representation of a D&D character.

    The class only stores information required to perform maths for skill
    checks, saving throws, and ability checks.  Consumers can extend it or
    wrap it in domain specific models as needed.
    """

    name: str
    level: int
    abilities: AbilityScores
    proficient_skills: Set[str] = field(default_factory=set)
    expertise_skills: Set[str] = field(default_factory=set)
    proficient_saves: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Character name cannot be empty")
        self._validate_level(self.level)
        self._normalise_sets()

    @staticmethod
    def _validate_level(level: int) -> None:
        proficiency_bonus(level)  # validation only

    def _normalise_sets(self) -> None:
        self.proficient_skills = {skill.lower() for skill in self.proficient_skills}
        self.expertise_skills = {skill.lower() for skill in self.expertise_skills}
        self.proficient_saves = {ability.lower() for ability in self.proficient_saves}

    @property
    def proficiency_bonus(self) -> int:
        return proficiency_bonus(self.level)

    def ability_modifier(self, ability: str) -> int:
        return self.abilities.modifier(ability)

    def skill_modifier(self, skill: str) -> int:
        key = skill.lower()
        try:
            ability = SKILL_ABILITIES[key]
        except KeyError as exc:
            raise KeyError(f"Unknown skill: {skill!r}") from exc
        mod = self.ability_modifier(ability)
        if key in self.expertise_skills:
            mod += 2 * self.proficiency_bonus
        elif key in self.proficient_skills:
            mod += self.proficiency_bonus
        return mod

    def saving_throw_modifier(self, ability: str) -> int:
        key = ability.lower()
        if key not in ABILITY_NAMES:
            raise KeyError(f"Unknown ability: {ability!r}")
        mod = self.ability_modifier(key)
        if key in self.proficient_saves:
            mod += self.proficiency_bonus
        return mod

    def ability_check(self, ability: str, *, bonus: int = 0) -> int:
        return self.ability_modifier(ability) + bonus

    def passive_score(self, skill: str) -> int:
        """Return the passive score for ``skill`` (10 + modifier)."""

        return 10 + self.skill_modifier(skill)
