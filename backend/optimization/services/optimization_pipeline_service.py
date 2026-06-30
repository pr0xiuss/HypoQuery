from psycopg import Connection

from backend.repositories.optimization_run_repo import (
    OptimizationRunRepository,
)
from backend.execution.observability.repositories.pipeline_log_repo import (
    PipelineLogRepository,
)
from backend.repositories.optimization_result_repo import (
    OptimizationResultRepository,
)
from uuid import uuid4

from backend.models.enums import (
    ClassifierRoute,
    LogLevel,
    PipelineStatus,
    QueryType,
    QueryCategory,
    RemediationType,
    ValidationStatus,
)
from backend.optimization.models.optimization_run import (
    OptimizationRun,
)
from backend.execution.observability.models.pipeline_log import (
    PipelineLog,
)
from backend.optimization.models.optimization_result import (
    OptimizationResult,
)
from backend.execution.observability.services.observability_service import (
    ObservabilityService,
)
from dataclasses import asdict


class OptimizationPipelineService:

    def __init__(
        self,
        connection: Connection,
    ):

        self.connection = connection

        self.run_repository = OptimizationRunRepository(connection)

        self.log_repository = PipelineLogRepository(connection)

        self.result_repository = OptimizationResultRepository(connection)

        self.observability = ObservabilityService(connection)

    def start_run(
        self,
        query,
        original_cost: float,
    ) -> int:

        match query.category:

            case (
                QueryCategory.SEQUENTIAL_SCAN
                | QueryCategory.JOIN
                | QueryCategory.AGGREGATION
                | QueryCategory.SORTING
                | QueryCategory.JSONB
                | QueryCategory.SUBQUERY
                | QueryCategory.INDEXING
            ):
                query_type = QueryType.SELECT

            case _:
                query_type = QueryType.OTHER

        run = OptimizationRun(
            trace_id=uuid4(),
            query_signature=query.id,
            query_type=query_type,
            classifier_route=ClassifierRoute.INDEX_SUGGESTER,
            pipeline_status=PipelineStatus.RUNNING,
            original_cost=original_cost,
        )

        run_id = self.run_repository.create(run)

        self.connection.commit()

        return run_id

    def log(
        self,
        run_id: int,
        node_name: str,
        message: str,
    ):

        log = PipelineLog(
            run_id=run_id,
            service_name="Observability",
            node_name=node_name,
            log_level=LogLevel.INFO,
            message=message,
        )

        self.log_repository.save(log)

        self.connection.commit()

    def save_findings(
        self,
        run_id: int,
        findings,
        execution_plan,
    ):

        for finding in findings:

            result = OptimizationResult(
                run_id=run_id,
                diagnosis=finding.issue,
                remediation_type=RemediationType.INDEX,
                validation_status=ValidationStatus.PENDING,
                original_explain_plan=asdict(execution_plan),
            )

            self.result_repository.save(result)

        self.connection.commit()

    def complete_run(
        self,
        run_id: int,
        optimized_cost: float,
    ):

        self.run_repository.mark_completed(
            run_id,
            optimized_cost,
            0.0,
        )

        self.connection.commit()

    def fail_run(
        self,
        run_id: int,
    ):

        self.run_repository.mark_failed(run_id)

        self.connection.commit()

    def optimize(
        self,
        query,
    ):

        run_id = None

        try:

            run_id = self.start_run(
                query=query,
                original_cost=0,
            )

            self.log(
                run_id,
                "Pipeline",
                "Optimization started",
            )

            plan, findings = self.observability.analyze_query(
                query,
            )

            self.save_findings(
                run_id,
                findings,
                plan,
            )

            self.complete_run(
                run_id,
                optimized_cost=plan.total_cost,
            )

            return plan, findings

        except Exception:

            if run_id is not None:
                self.fail_run(run_id)

            raise
