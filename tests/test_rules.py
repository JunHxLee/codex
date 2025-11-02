import random

from dndrules import rules


def test_resolve_check_success_and_failure():
    rng = random.Random(42)
    success = rules.resolve_check(5, dc=10, rng=rng)
    assert isinstance(success.total, int)
    assert success.modifier == 5
    assert success.dc == 10

    rng.seed(42)
    failure = rules.resolve_check(-1, dc=20, rng=rng)
    assert not failure.success
    assert failure.natural == failure.roll_details[0]


def test_resolve_contest_determines_winner():
    rng = random.Random(7)
    outcome = rules.resolve_contest(4, 1, rng=rng)
    assert outcome.winner in {"a", "b", None}
    # Deterministic expectation with the chosen seed.
    assert outcome.winner == ("a" if outcome.total_a > outcome.total_b else "b" if outcome.total_b > outcome.total_a else None)
    assert outcome.check_a.roll_details
    assert outcome.check_b.roll_details
