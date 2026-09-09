import pytest
from datetime import datetime, timedelta, timezone

from backend.platform.scheduler.application.retry_policy import DefaultRetryClassifier, ExponentialBackoffRetryPolicy
from backend.platform.scheduler.domain.job import Job, JobType, JobStatus
from backend.execution.runtime.system_clock import SystemClock


class MockClock(SystemClock):
    def __init__(self, now_time: datetime):
        self._now = now_time

    def now(self) -> datetime:
        return self._now

    def monotonic(self) -> float:
        return 0.0


def test_default_classifier_is_retryable():
    classifier = DefaultRetryClassifier()
    assert classifier.is_retryable("ConnectionError") is True
    assert classifier.is_retryable("TimeoutError") is True
    assert classifier.is_retryable("OperationalError") is True
    assert classifier.is_retryable("ValueError") is False
    assert classifier.is_retryable(None) is False


def test_exponential_backoff_first_failure():
    classifier = DefaultRetryClassifier()
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    clock = MockClock(now)
    policy = ExponentialBackoffRetryPolicy(classifier, clock, base_delay_seconds=5)

    job = Job(
        name="test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        status=JobStatus.FAILED,
        attempt_count=1,
        max_attempts=3
    )

    next_attempt = policy.calculate_next_attempt(job, "ConnectionError")
    
    assert next_attempt is not None
    # 2^0 * 5 = 5 seconds
    assert next_attempt == now + timedelta(seconds=5)


def test_exponential_backoff_second_failure():
    classifier = DefaultRetryClassifier()
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    clock = MockClock(now)
    policy = ExponentialBackoffRetryPolicy(classifier, clock, base_delay_seconds=5)

    job = Job(
        name="test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        status=JobStatus.FAILED,
        attempt_count=2,
        max_attempts=3
    )

    next_attempt = policy.calculate_next_attempt(job, "ConnectionError")
    
    assert next_attempt is not None
    # 2^1 * 5 = 10 seconds
    assert next_attempt == now + timedelta(seconds=10)


def test_exponential_backoff_max_attempts_exhausted():
    classifier = DefaultRetryClassifier()
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    clock = MockClock(now)
    policy = ExponentialBackoffRetryPolicy(classifier, clock, base_delay_seconds=5)

    job = Job(
        name="test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        status=JobStatus.FAILED,
        attempt_count=3,
        max_attempts=3
    )

    next_attempt = policy.calculate_next_attempt(job, "ConnectionError")
    
    # Should not retry if attempt_count >= max_attempts
    assert next_attempt is None


def test_exponential_backoff_non_retryable_error():
    classifier = DefaultRetryClassifier()
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    clock = MockClock(now)
    policy = ExponentialBackoffRetryPolicy(classifier, clock, base_delay_seconds=5)

    job = Job(
        name="test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        status=JobStatus.FAILED,
        attempt_count=1,
        max_attempts=3
    )

    next_attempt = policy.calculate_next_attempt(job, "ValueError")
    
    assert next_attempt is None
