from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.graph_snapshot import (
    GraphSnapshot,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)


@dataclass(frozen=True, slots=True)
class RetrievalJob:
    """
    Represents one retrieval request against a projected
    Knowledge Graph.
    """

    graph: GraphSnapshot

    objective: RetrievalObjective