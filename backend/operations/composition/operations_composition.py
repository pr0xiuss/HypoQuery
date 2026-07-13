from __future__ import annotations


class OperationsComposition:
    """
    Composition root for the Operations
    bounded context.

    Module 1 intentionally exposes an empty
    composition root. Subsequent modules will
    register Case Management, Verification,
    Operational Assessment, Monitoring and
    Policy Evaluation services here.
    """

    pass