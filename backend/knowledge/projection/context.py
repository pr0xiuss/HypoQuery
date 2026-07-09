from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.knowledge_graph import KnowledgeGraph
from backend.knowledge.projection.job import ProjectionJob


@dataclass(slots=True)
class ProjectionContext:
    """
    Mutable state shared across the projection pipeline.

    ProjectionContext accumulates projected knowledge while
    handlers transform immutable execution records into
    graph entities.
    """

    job: ProjectionJob

    graph: KnowledgeGraph = field(
        default_factory=KnowledgeGraph,
    )