from unittest.mock import Mock

from backend.observability.persistence.persistence_subscriber import (
    PersistenceSubscriber,
)


def test_delegates_to_repository():
    repository = Mock()

    subscriber = PersistenceSubscriber(
        repository,
    )

    event = Mock()

    subscriber.handle(
        event,
    )

    repository.save.assert_called_once_with(
        event,
    )