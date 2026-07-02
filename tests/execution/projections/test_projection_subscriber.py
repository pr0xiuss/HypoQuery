from unittest.mock import Mock

from backend.execution.projections.projection_subscriber import (
    ProjectionSubscriber,
)


def test_delegates_to_builder():
    builder = Mock()

    subscriber = ProjectionSubscriber(
        builder,
    )

    event = Mock()

    subscriber.handle(
        event,
    )

    builder.apply.assert_called_once_with(
        event,
    )