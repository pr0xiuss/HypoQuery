from __future__ import annotations

from uuid import uuid4

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
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
            job_id = uuid4()
            trace_id = uuid4()

            execution = PipelineExecution(
                job=PipelineJob(
                    source="benchmark",
                    pipeline_version="1.0",
                    job_id=job_id,
                    trace_id=trace_id,
                ),
                context=PipelineContext(
                    execution_id=job_id,
                    trace_id=trace_id,
                    pipeline_name="optimization",
                    pipeline_version="1.0",
                    database="hypoquery",
                    schema="public",
                ),
            )

            execution.state.add_artifact(
                "query",
                query,
            )

            executions.append(execution)

        return executions