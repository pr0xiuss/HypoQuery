from uuid import UUID

from .execution_projection import ExecutionProjection


class ExecutionProjectionStore:
    """
    Stores execution projections indexed by execution ID.
    """

    def __init__(self) -> None:
        self._projections: dict[
            UUID,
            ExecutionProjection,
        ] = {}

    def save(
        self,
        projection: ExecutionProjection,
    ) -> None:
        self._projections[
            projection.execution_id
        ] = projection

    def get(
        self,
        execution_id: UUID,
    ) -> ExecutionProjection | None:
        return self._projections.get(
            execution_id,
        )

    def all(
        self,
    ) -> list[ExecutionProjection]:
        return list(
            self._projections.values()
        )

    def clear(
        self,
    ) -> None:
        self._projections.clear()