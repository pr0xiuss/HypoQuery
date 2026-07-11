from __future__ import annotations

from dataclasses import dataclass, field

from backend.knowledge.models.node_key import NodeKey
from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)


@dataclass(slots=True)
class EvidenceSet:
    """
    Mutable collection of evidence accumulated during one
    retrieval execution.

    Retrievers contribute evidence to the same set.
    """

    items: list[
        Evidence
    ] = field(
        default_factory=list,
    )

    def add(
        self,
        evidence: Evidence,
    ) -> None:

        self.items.append(
            evidence,
        )

    def extend(
        self,
        evidence: list[
            Evidence,
        ],
    ) -> None:

        self.items.extend(
            evidence,
        )

    def __iter__(
        self,
    ):

        return iter(
            self.items,
        )


    def __len__(
        self,
    ) -> int:

        return len(
            self.items,
        )


    def contains(
        self,
        key: NodeKey,
    ) -> bool:

        return any(
            evidence.key == key
            for evidence in self.items
        )


    def deduplicate(
        self,
    ) -> None:

        unique: dict[
            NodeKey,
            Evidence,
        ] = {}

        for evidence in self.items:

            unique.setdefault(
                evidence.key,
                evidence,
            )

        self.items = list(
            unique.values(),
        )

    def sort(
        self,
    ) -> None:

        self.items.sort(
            key=lambda evidence: (
                -evidence.confidence,
                evidence.key.value,
            )
        )