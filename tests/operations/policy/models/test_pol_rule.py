from backend.operations.policy.models.rule import (
    PolicyRule,
)


def test_policy_rule() -> None:
    rule = PolicyRule(
        name="Regression Threshold",
        threshold=5.0,
        description="Reopen when degradation exceeds 5%.",
    )

    assert rule.name == "Regression Threshold"
    assert rule.threshold == 5.0
    assert (
        rule.description
        == "Reopen when degradation exceeds 5%."
    )