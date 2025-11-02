import random

import pytest

from dndrules import dice


def test_parse_expression_handles_modifier_only():
    parsed = dice.parse_expression("+5")
    assert parsed.dice == ()
    assert parsed.modifier_total == 5


def test_roll_returns_total_and_breakdown():
    rng = random.Random(1)
    result = dice.roll("2d6+1", rng=rng)
    assert result.total == sum(result.dice_results[0]) + 1
    assert result.modifiers == (1,)
    assert result.detail().endswith(f"= {result.total}")


def test_expected_value_matches_simple_probability():
    assert dice.expected_value("1d6") == pytest.approx(3.5)
    assert dice.expected_value("2d4+2") == pytest.approx(2 * 2.5 + 2)


def test_advantage_and_disadvantage_rolls():
    rng = random.Random(5)
    adv, detail_adv = dice.roll_with_advantage(rng=rng)
    rng.seed(5)
    disadv, detail_disadv = dice.roll_with_disadvantage(rng=rng)
    assert adv >= max(detail_adv)
    assert disadv <= min(detail_disadv)
    assert len(detail_adv) == len(detail_disadv) == 2
