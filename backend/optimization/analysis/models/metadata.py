from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class FindingMetadata:
    """
    Additional structured information associated with a finding.

    This metadata provides supporting information for
    downstream recommendation generation while remaining
    generic and extensible.
    """

    attributes: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.attributes.get(key, default)

    def contains(self, key: str) -> bool:
        return key in self.attributes