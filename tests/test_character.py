import pytest

from dndrules import abilities, character


def make_character():
    scores = abilities.AbilityScores(
        strength=15,
        dexterity=16,
        constitution=14,
        intelligence=12,
        wisdom=10,
        charisma=8,
    )
    return character.Character(
        name="Nyx",
        level=5,
        abilities=scores,
        proficient_skills={"stealth", "acrobatics"},
        expertise_skills={"stealth"},
        proficient_saves={"dexterity"},
    )


def test_proficiency_bonus_progression():
    assert character.proficiency_bonus(1) == 2
    assert character.proficiency_bonus(5) == 3
    assert character.proficiency_bonus(13) == 5
    assert character.proficiency_bonus(20) == 6
    with pytest.raises(ValueError):
        character.proficiency_bonus(0)


def test_skill_and_save_modifiers():
    rogue = make_character()
    assert rogue.skill_modifier("stealth") == abilities.modifier(rogue.abilities.dexterity) + 2 * rogue.proficiency_bonus
    assert rogue.skill_modifier("acrobatics") == abilities.modifier(rogue.abilities.dexterity) + rogue.proficiency_bonus
    assert rogue.saving_throw_modifier("dexterity") == abilities.modifier(rogue.abilities.dexterity) + rogue.proficiency_bonus
    assert rogue.saving_throw_modifier("wisdom") == abilities.modifier(rogue.abilities.wisdom)
    with pytest.raises(KeyError):
        rogue.skill_modifier("cooking")


def test_passive_score_uses_skill_modifier():
    rogue = make_character()
    assert rogue.passive_score("perception") == 10 + rogue.skill_modifier("perception")
