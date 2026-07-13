from __future__ import annotations


class OperationsError(Exception):
    """
    Base exception for the Operations
    bounded context.
    """


class CaseError(OperationsError):
    """
    Raised when Optimization Case operations fail.
    """


class VerificationError(OperationsError):
    """
    Raised when verification fails.
    """


class OperationalAssessmentError(OperationsError):
    """
    Raised when operational assessment fails.
    """


class MonitoringError(OperationsError):
    """
    Raised when monitoring operations fail.
    """


class PolicyEvaluationError(OperationsError):
    """
    Raised when policy evaluation fails.
    """