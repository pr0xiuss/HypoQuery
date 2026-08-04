from pydantic import BaseModel
from pydantic import ConfigDict


class DatabaseStatisticsResult(BaseModel):
    """
    Database-level statistics.
    """

    transactions_committed: int
    transactions_rolled_back: int

    blocks_read: int
    blocks_hit: int

    tuples_returned: int
    tuples_fetched: int

    tuples_inserted: int
    tuples_updated: int
    tuples_deleted: int

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )