import pytest

from dndrules import abilities


def test_modifier_table_matches_known_values():
    assert abilities.modifier(10) == 0
    assert abilities.modifier(8) == -1
    assert abilities.modifier(18) == 4


def test_validate_score_enforces_bounds():
    with pytest.raises(ValueError):
        abilities.validate_score(0)
    with pytest.raises(ValueError):
        abilities.validate_score(40)


def test_ability_scores_helper_methods():
    scores = abilities.AbilityScores(15, 14, 13, 12, 10, 8)
    assert scores.modifier("strength") == 2
    assert scores.to_dict()["charisma"] == 8
    with pytest.raises(KeyError):
        scores.modifier("luck")

    data = {name: 10 for name in abilities.ABILITY_NAMES}
    recreated = abilities.AbilityScores.from_mapping(data)
    assert recreated.dexterity == 10
