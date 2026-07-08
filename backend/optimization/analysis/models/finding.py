from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4

from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity


@dataclass(slots=True)
class Finding:
    """
    Represents a deterministic observation produced by Analysis.

    A Finding answers the question:

        "What did we observe?"

    It never suggests solutions or recommendations.
    """

    category: FindingCategory
    code: str
    title: str
    description: str
    severity: FindingSeverity

    location: FindingLocation = field(default_factory=FindingLocation)
    metadata: FindingMetadata = field(default_factory=FindingMetadata)

    id: UUID = field(default_factory=uuid4)
    observed_at: datetime = field(default_factory=lambda: datetime.now(UTC))