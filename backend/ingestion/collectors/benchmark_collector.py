from __future__ import annotations

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.contracts.job import PipelineJob

from backend.ingestion.query_catalog import QueryCatalog

from .base_collector import BaseCollector


class BenchmarkCollector(BaseCollector):
    """
    Collects benchmark queries and converts them into PipelineExecution
    instances.
    """

    def __init__(self, catalog: QueryCatalog, ) -> None:

        self._catalog = catalog

    def collect(self) -> list[PipelineExecution]:

        executions: list[PipelineExecution] = []

        for query in self._catalog.all():

            execution = PipelineExecution(
                job=PipelineJob(
                    source="benchmark",
                    pipeline_version="1.0",
                ),
                context=PipelineContext(
                    fingerprint=QueryFingerprint(
                        normalized_sql=query.sql,
                        hash=query.id,
                    ),
                    database="benchmark",
                    schema="public",
                ),
            )

            execution.state.add_artifact(
                "query",
                query,
            )

            executions.append(execution)

        return executions