from backend.knowledge.retrieval.handlers.recommendation_retriever import (
    RecommendationRetriever,
)
from backend.knowledge.retrieval.registry.retrieval_registry import (
    RetrievalRegistry,
)


def test_retrieval_registry():

    registry = RetrievalRegistry()

    retriever = RecommendationRetriever()

    registry.register(
        retriever,
    )

    retrievers = registry.all()

    assert len(
        retrievers,
    ) == 1

    assert retrievers[0] is retriever