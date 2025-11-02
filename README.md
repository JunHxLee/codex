# dndrules

Lightweight Python helpers for working with Dungeons & Dragons 5th Edition
mechanics.  The package is designed for bots, web services, and hobby
projects that need a straightforward way to roll dice, calculate ability
modifiers, or resolve contested checks without re-implementing the math
from scratch.

## Features

- Parse and roll common dice expressions (``2d6+3``, ``d20-1``) with access
  to the raw roll results.
- Compute ability modifiers and manage the six standard ability scores.
- Model basic character information including skill proficiency, expertise,
  and saving throws.
- Resolve ability checks, saving throws, and contests with advantage or
  disadvantage support.

## Installation

```bash
pip install .
```

## 사용법

```python
from dndrules import abilities, character, dice, rules

# 캐릭터 능력치 설정
scores = abilities.AbilityScores(
    strength=15,
    dexterity=12,
    constitution=14,
    intelligence=10,
    wisdom=13,
    charisma=8,
)

# 캐릭터 인스턴스 생성
rogue = character.Character(
    name="Nyx",
    level=5,
    abilities=scores,
    proficient_skills={"stealth", "acrobatics"},
    expertise_skills={"stealth"},
    proficient_saves={"dexterity", "intelligence"},
)

# 기술 판정 굴리기 (은신)
stealth_bonus = rogue.skill_modifier("stealth")
result = rules.resolve_check(stealth_bonus, dc=15)
print(result.total, result.success)

# 대결 판정 계산 (은신 vs. 상대 보정치 3)
contest = rules.resolve_contest(rogue.skill_modifier("stealth"), modifier_b=3)
print(contest.winner)
```

## Running the tests

```bash
pytest
```
