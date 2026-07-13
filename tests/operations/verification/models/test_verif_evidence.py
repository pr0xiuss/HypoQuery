from backend.operations.verification.models.evidence import (
    VerificationEvidence,
)


def test_verification_evidence() -> None:
    evidence = VerificationEvidence(
        execution_plan_changed=True,
        planner_changed=True,
        metrics={
            "execution_time": 12.4,
            "shared_buffers": 18.0,
        },
    )

    assert evidence.execution_plan_changed
    assert evidence.planner_changed

    assert evidence.metrics["execution_time"] == 12.4
    assert evidence.metrics["shared_buffers"] == 18.0