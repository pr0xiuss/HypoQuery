from __future__ import annotations

from backend.knowledge.retrieval.engine import (
    RetrievalEngine,
)
from backend.knowledge.retrieval.filters.graph_filter import (
    GraphFilter,
)
from backend.knowledge.retrieval.filters.node_filter import (
    NodeFilter,
)
from backend.knowledge.retrieval.handlers.finding_retriever import (
    FindingRetriever,
)
from backend.knowledge.retrieval.handlers.graph_expansion_retriever import (
    GraphExpansionRetriever,
)
from backend.knowledge.retrieval.handlers.recommendation_retriever import (
    RecommendationRetriever,
)
from backend.knowledge.retrieval.handlers.strategy_retriever import (
    StrategyRetriever,
)
from backend.knowledge.retrieval.handlers.validation_retriever import (
    ValidationRetriever,
)
from backend.knowledge.retrieval.registry.retrieval_registry import (
    RetrievalRegistry,
)
from backend.knowledge.retrieval.service import (
    RetrievalService,
)


def build_retrieval_service() -> RetrievalService:
    """
    Builds the complete deterministic retrieval pipeline.
    """

    graph_filter = GraphFilter(
        node_filter=NodeFilter(),
    )

    registry = RetrievalRegistry()

    registry.register(
        FindingRetriever(),
    )

    registry.register(
        RecommendationRetriever(),
    )

    registry.register(
        ValidationRetriever(),
    )

    registry.register(
        StrategyRetriever(),
    )

    registry.register(
        GraphExpansionRetriever(),
    )

    engine = RetrievalEngine(
        registry=registry,
    )

    return RetrievalService(
        engine=engine,
    )