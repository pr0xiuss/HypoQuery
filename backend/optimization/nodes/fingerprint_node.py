from __future__ import annotations

import hashlib

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.contracts.node_result import NodeResult
from backend.execution.pipeline.base_node import PipelineNode


class FingerprintNode(PipelineNode):
    """
    Computes a deterministic query fingerprint.
    """

    @property
    def name(self) -> str:
        return "fingerprint"

    def execute(self, execution: PipelineExecution,) -> NodeResult:

        sql = execution.state.normalized_sql

        if sql is None:
            return NodeResult.failure(
                "Normalized SQL missing."
            )

        execution.state.fingerprint = QueryFingerprint(
            normalized_sql=sql,
            hash=hashlib.sha256(
                sql.encode()
            ).hexdigest(),
        )

        return NodeResult.success()