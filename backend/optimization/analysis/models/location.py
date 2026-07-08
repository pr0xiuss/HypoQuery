from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class FindingLocation:
    """
    Identifies where a finding originated.

    A finding may point to an execution plan node,
    a table, an index, or another database object.
    """

    node_id: Optional[int] = None
    relation: Optional[str] = None
    schema: Optional[str] = None
    index: Optional[str] = None
    column: Optional[str] = None