"""Lightweight Dungeons & Dragons 5e rules helpers.

This package exposes small, easy-to-compose utilities that cover the
most common mechanical building blocks found in D&D 5e games:

* :mod:`dndrules.dice` – parsing and rolling dice notation.
* :mod:`dndrules.abilities` – working with ability scores and modifiers.
* :mod:`dndrules.character` – character level math, including
  proficiency bonuses and skill modifiers.
* :mod:`dndrules.rules` – convenience helpers for resolving checks and
  contests.

The modules are intentionally small and dependency free so they can be
embedded in a CLI helper, a Discord bot, or a campaign manager.
"""

from . import abilities, character, dice, rules

__all__ = ["abilities", "character", "dice", "rules"]
